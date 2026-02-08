"""
Daily Spanish Verb Trainer – reply ingestion via IMAP.
Monitors inbox for replies to daily exercise emails and extracts Spanish sentences.
"""

import os
import re
import imaplib
import email
from email.header import decode_header

# Env: IMAP_HOST, IMAP_PORT, EMAIL_USER, EMAIL_PASSWORD
def _env(key: str, default: str = "") -> str:
    return (os.environ.get(key) or default).strip()

IMAP_HOST = _env("IMAP_HOST") or "imap.gmail.com"
IMAP_PORT = int(_env("IMAP_PORT") or "993")
EMAIL_USER = _env("EMAIL_USER")
EMAIL_PASSWORD = _env("EMAIL_PASSWORD")

SUBJECT_PREFIX = "Spanish Verb – "
# Patterns that indicate start of quoted/original message (strip everything after)
QUOTE_PATTERNS = [
    r"\n\s*On\s+.+wrote:\s*$",
    r"\n-{3,}\s*Original Message\s*-{3,}",
    r"\n_{3,}",
    r"\nFrom:\s*.+Sent:\s*.+To:\s*",
    r"\nEl\s+.+escribió:\s*$",
    r"\n>\s*",
    r"\nFrom:.*\nSent:.*\nTo:",
    r"\n_{5,}",
]
QUOTE_REGEX = re.compile("|".join(f"({p})" for p in QUOTE_PATTERNS), re.IGNORECASE | re.DOTALL)


def _decode_mime_header(header: str | None) -> str:
    if not header:
        return ""
    decoded = decode_header(header)
    parts = []
    for part, charset in decoded:
        if isinstance(part, bytes):
            parts.append(part.decode(charset or "utf-8", errors="replace"))
        else:
            parts.append(part or "")
    return " ".join(parts)


def _get_body(msg: email.message.Message) -> str:
    """Extract plain text body from email message."""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            if ctype == "text/plain":
                raw = part.get_payload(decode=True)
                if raw:
                    charset = part.get_content_charset() or "utf-8"
                    body = raw.decode(charset, errors="replace")
                break
    else:
        raw = msg.get_payload(decode=True)
        if raw:
            charset = msg.get_content_charset() or "utf-8"
            body = raw.decode(charset, errors="replace")
    return body


def _strip_quoted_and_signature(text: str) -> str:
    """Remove quoted reply and signature from email body."""
    # Remove content after quote markers
    match = QUOTE_REGEX.search(text)
    if match:
        text = text[: match.start()].strip()
    # Common signature delimiters
    for delim in ["-- ", "\n--\n", "\n___", "\n---", "\nSaludos,", "\nGracias,"]:
        idx = text.find(delim)
        if idx != -1:
            text = text[:idx].strip()
    return text.strip()


def _extract_sentences(text: str, max_sentences: int = 5) -> list[str]:
    """
    Extract ordered Spanish sentences from reply body.
    Expects user to write one sentence per line (optionally with 1. 2. etc.).
    """
    lines = []
    for line in text.splitlines():
        line = line.strip()
        # Remove leading numbering (1. 2. 1) 2) etc.)
        line = re.sub(r"^\s*\d+[.)]\s*", "", line).strip()
        if not line:
            continue
        # Skip lines that are clearly not Spanish sentences (only punctuation, or "yo" "tú" alone)
        if re.match(r"^[\s\W]+$", line):
            continue
        if line.lower() in ("yo", "tú", "él", "ella", "nosotros", "nosotras", "ellos", "ellas"):
            continue
        # Accept lines that look like sentences (contain letters, possibly accents)
        if re.search(r"[a-zA-ZáéíóúñÁÉÍÓÚÑ]", line) and len(line) > 2:
            lines.append(line)
            if len(lines) >= max_sentences:
                break
    return lines[:max_sentences]


def is_reply_to_exercise(subject: str) -> bool:
    """True if this email is a reply to our daily exercise (not the feedback email)."""
    if not subject:
        return False
    subj = _decode_mime_header(subject)
    # Reply subject is often "Re: Spanish Verb – LLEVAR (Preterite)"
    if "Re:" in subj and SUBJECT_PREFIX in subj and "Feedback" not in subj:
        return True
    if subj.startswith("Re:") and "Spanish Verb" in subj and "Feedback" not in subj:
        return True
    return False


def fetch_replies(limit: int = 10) -> list[dict]:
    """
    Connect via IMAP, fetch recent emails that look like replies to our exercise.
    Returns list of dicts: { subject, body_clean, sentences, message_id }.
    """
    if not EMAIL_USER or not EMAIL_PASSWORD:
        raise ValueError("EMAIL_USER and EMAIL_PASSWORD must be set")
    results = []
    mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    try:
        mail.login(EMAIL_USER, EMAIL_PASSWORD)
        mail.select("INBOX")
        # Search all recent (or UNSEEN to process only new)
        status, data = mail.search(None, "ALL")
        if status != "OK":
            return results
        ids = data[0].split()
        # Process newest first
        for uid in reversed(ids[-limit * 2 :]):
            try:
                status, msg_data = mail.fetch(uid, "(RFC822)")
                if status != "OK" or not msg_data:
                    continue
                raw = msg_data[0][1]
                msg = email.message_from_bytes(raw)
                subj = msg.get("Subject", "")
                if not is_reply_to_exercise(subj):
                    continue
                body = _get_body(msg)
                body_clean = _strip_quoted_and_signature(body)
                sentences = _extract_sentences(body_clean, max_sentences=5)
                if not sentences:
                    continue
                msg_id = msg.get("Message-ID", "")
                results.append({
                    "subject": _decode_mime_header(subj),
                    "body_clean": body_clean,
                    "sentences": sentences,
                    "message_id": msg_id,
                    "uid": uid,
                })
            except Exception:
                continue
            if len(results) >= limit:
                break
    finally:
        try:
            mail.logout()
        except Exception:
            pass
    return results


def mark_as_read(uid: bytes) -> None:
    """Mark message as read (optional, for IMAP)."""
    mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    try:
        mail.login(EMAIL_USER, EMAIL_PASSWORD)
        mail.select("INBOX")
        mail.store(uid, "+FLAGS", "\\Seen")
    finally:
        try:
            mail.logout()
        except Exception:
            pass
