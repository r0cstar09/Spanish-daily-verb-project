"""
Daily Spanish Verb Trainer – outbound email.
Sends the daily exercise email only (evaluate in ChatGPT or elsewhere).
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, make_msgid

# Env: SMTP_HOST, SMTP_PORT, EMAIL_USER, EMAIL_PASSWORD, TARGET_EMAIL
def _env(key: str, default: str = "") -> str:
    return (os.environ.get(key) or default).strip()

SMTP_HOST = _env("SMTP_HOST") or "smtp.gmail.com"
SMTP_PORT = int(_env("SMTP_PORT") or "587")
EMAIL_USER = _env("EMAIL_USER")
EMAIL_PASSWORD = _env("EMAIL_PASSWORD")
TARGET_EMAIL = _env("TARGET_EMAIL")

SUBJECT_PREFIX = "Spanish Verb – "


def _smtp_send(to: str, subject: str, body_plain: str, body_html: str | None = None):
    if not EMAIL_USER or not EMAIL_PASSWORD:
        raise ValueError("EMAIL_USER and EMAIL_PASSWORD must be set")
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = formataddr(("Spanish Verb Trainer", EMAIL_USER))
    msg["To"] = to
    msg["Message-ID"] = make_msgid(domain="spanish-verb-trainer")
    msg.attach(MIMEText(body_plain, "plain", "utf-8"))
    if body_html:
        msg.attach(MIMEText(body_html, "html", "utf-8"))
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_USER, EMAIL_PASSWORD)
        smtp.sendmail(EMAIL_USER, to, msg.as_string())


def build_daily_exercise_body(verb: str, assignments: list[dict]) -> tuple[str, str]:
    """Plain and HTML body for the daily exercise email (mixed tenses per pronoun)."""
    verb_upper = verb.upper()
    lines = [f"{i+1}. {a['pronoun']} ({a['tense']})" for i, a in enumerate(assignments)]
    plain = f"""Daily Spanish Verb Practice

Verb: {verb_upper}

Write ONE sentence for each line (pronoun + tense). Use the verb in the tense shown:

{chr(10).join(lines)}

Practice your 5 sentences and get evaluated in ChatGPT or however you like.
"""
    ol_items = "".join(f"<li>{a['pronoun']} — <strong>{a['tense']}</strong></li>" for a in assignments)
    html = f"""<html><body style="font-family: sans-serif;">
<h2>Daily Spanish Verb Practice</h2>
<p><strong>Verb:</strong> {verb_upper}</p>
<p>Write ONE sentence for each line. Use the verb in the tense shown:</p>
<ol>
{ol_items}
</ol>
<p>Practice your 5 sentences and get evaluated in ChatGPT or however you like.</p>
</body></html>"""
    return plain, html


def send_daily_exercise(verb: str, assignments: list[dict], to: str | None = None) -> None:
    """Send the daily exercise email to the target address."""
    to = to or TARGET_EMAIL
    if not to:
        raise ValueError("TARGET_EMAIL must be set or pass to=")
    subject = f"{SUBJECT_PREFIX}{verb.upper()} (mixed tenses)"
    plain, html = build_daily_exercise_body(verb, assignments)
    _smtp_send(to, subject, plain, html)
