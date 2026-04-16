"""
Daily Spanish Verb Trainer – outbound email.
Sends conjugation exercise + sentence-bank practice (evaluate in ChatGPT or elsewhere).
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, make_msgid

from native_lessons import LESSON_TITLE
from sentence_rotation import SENTENCES_PER_EMAIL
from verb_selector import TRACK_IRREGULAR, TRACK_PARETO

# Env: SMTP_HOST, SMTP_PORT, EMAIL_USER, EMAIL_PASSWORD, TARGET_EMAIL
def _env(key: str, default: str = "") -> str:
    return (os.environ.get(key) or default).strip()

SMTP_HOST = _env("SMTP_HOST") or "smtp.gmail.com"
SMTP_PORT = int(_env("SMTP_PORT") or "587")
EMAIL_USER = _env("EMAIL_USER")
EMAIL_PASSWORD = _env("EMAIL_PASSWORD")
TARGET_EMAIL = _env("TARGET_EMAIL")

# When sentence count exceeds this, attach plain text instead of inlining all lines.
SENTENCE_ATTACHMENT_THRESHOLD = 60

_CATEGORY_LABEL = {
    "pareto_regular": "Pareto (high-frequency regular)",
    "irregular": "irregular",
    "stem_changing": "stem-changing",
}


def _subject_for_track(verb: str, track: str) -> str:
    vu = verb.upper()
    if track == TRACK_PARETO:
        return f"Spanish Verb – Pareto: {vu} (all tenses + sentences)"
    return f"Spanish Verb – Irregular / stem: {vu} (all tenses + sentences)"


def _smtp_send(
    to: str,
    subject: str,
    body_plain: str,
    body_html: str | None = None,
    *,
    attachment_plain: str | None = None,
    attachment_filename: str | None = None,
) -> None:
    if not EMAIL_USER or not EMAIL_PASSWORD:
        raise ValueError("EMAIL_USER and EMAIL_PASSWORD must be set")
    msg = MIMEMultipart("mixed")
    msg["Subject"] = subject
    msg["From"] = formataddr(("Spanish Verb Trainer", EMAIL_USER))
    msg["To"] = to
    msg["Message-ID"] = make_msgid(domain="spanish-verb-trainer")

    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(body_plain, "plain", "utf-8"))
    if body_html:
        alt.attach(MIMEText(body_html, "html", "utf-8"))
    msg.attach(alt)

    if attachment_plain is not None and attachment_filename:
        att = MIMEText(attachment_plain, "plain", "utf-8")
        att.add_header("Content-Disposition", "attachment", filename=attachment_filename)
        msg.attach(att)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_USER, EMAIL_PASSWORD)
        smtp.sendmail(EMAIL_USER, to, msg.as_string())


def build_daily_exercise_body(
    verb: str,
    assignments: list[dict],
    category: str = "",
    sentences: list[dict] | None = None,
    full_bank_size: int | None = None,
    native_lesson: str | None = None,
) -> tuple[str, str, str | None, str | None]:
    """
    Plain and HTML body; optional attachment (plain text) when sentence list is long.
    Returns (plain, html, attachment_plain_or_none, attachment_filename_or_none).
    """
    verb_upper = verb.upper()
    cat_label = _CATEGORY_LABEL.get(category, category.replace("_", "-")) if category else ""
    cat_note = f" ({cat_label} verb)" if cat_label else ""

    n_conj = len(assignments)
    lines = []
    for i, a in enumerate(assignments):
        trans = a.get("translation", "")
        if trans:
            lines.append(f"{i+1}. {a['pronoun']} ({a['tense']}) — {trans}")
        else:
            lines.append(f"{i+1}. {a['pronoun']} ({a['tense']})")

    sentences = sentences or []
    attach_plain: str | None = None
    attach_name: str | None = None

    sentence_lines_plain: list[str] = []
    sentence_lines_html: list[str] = []
    use_attachment = len(sentences) > SENTENCE_ATTACHMENT_THRESHOLD

    for i, s in enumerate(sentences, start=1):
        en = s.get("en", "").strip()
        sense = (s.get("sense") or "").strip()
        lesson = (s.get("lesson") or "").strip()
        if sense and lesson:
            tag_plain = f"[{sense} · {lesson}]"
            tag_html = (
                f'<span style="color:#444">[{sense}]</span> '
                f'<span style="color:#666;font-size:0.9em">({lesson})</span>'
            )
        elif sense:
            tag_plain = f"[{sense}]"
            tag_html = f'<span style="color:#444">[{sense}]</span>'
        elif lesson:
            tag_plain = f"[{lesson}]"
            tag_html = f'<span style="color:#666;font-size:0.9em">({lesson})</span>'
        else:
            tag_plain = ""
            tag_html = ""
        if tag_plain:
            sentence_lines_plain.append(f"{i}. {tag_plain} {en}")
            sentence_lines_html.append(f"<li><strong>{i}.</strong> {tag_html} {en}</li>")
        else:
            sentence_lines_plain.append(f"{i}. {en}")
            sentence_lines_html.append(f"<li><strong>{i}.</strong> {en}</li>")

    if use_attachment and sentences:
        attach_plain = "\n".join(sentence_lines_plain)
        attach_name = f"sentence-practice-{verb.lower()}.txt"

    if sentences and not use_attachment:
        n_today = len(sentences)
        fb = full_bank_size if full_bank_size is not None else n_today
        rot_note = ""
        if fb > n_today:
            rot_note = (
                f"\nToday you have {n_today} of {fb} prompts from the committed bank; "
                f"the next time this verb is scheduled, you will get a different set of "
                f"{SENTENCES_PER_EMAIL} (rotated by date and track).\n\n"
            )
        part2_plain = (
            "\n\nPart 2 — Sentence practice\n\n"
            "Translate each English prompt into natural Spanish using this verb. "
            "Number your translations to match.\n"
            + rot_note
            + "\n".join(sentence_lines_plain)
        )
        rot_html = ""
        if fb > n_today:
            rot_html = (
                f"<p>Today: <strong>{n_today}</strong> of <strong>{fb}</strong> prompts from the bank. "
                f"Next time this verb appears, you will see a different slice of {SENTENCES_PER_EMAIL} (rotated by date and track).</p>"
            )
        part2_html = (
            "<h3>Part 2 — Sentence practice</h3>"
            "<p>Translate each English prompt into natural Spanish using this verb. "
            "Number your translations to match.</p>"
            + rot_html
            + f"<ol style='margin-top:0.5em'>{''.join(sentence_lines_html)}</ol>"
        )
    elif sentences and use_attachment:
        part2_plain = (
            "\n\nPart 2 — Sentence practice\n\n"
            f"The sentence list ({len(sentences)} items) is attached as <strong>{attach_name}</strong> "
            f"because it exceeds {SENTENCE_ATTACHMENT_THRESHOLD} lines inline.\n"
        )
        part2_html = (
            "<h3>Part 2 — Sentence practice</h3>"
            f"<p>The sentence list ({len(sentences)} items) is attached as <strong>{attach_name}</strong> "
            f"because it exceeds {SENTENCE_ATTACHMENT_THRESHOLD} lines inline.</p>"
        )
    else:
        part2_plain = ""
        part2_html = ""

    part0_plain = ""
    part0_html = ""
    if native_lesson:
        part0_plain = (
            f"{LESSON_TITLE}:\n{native_lesson}\n\n"
        )
        part0_html = (
            f'<div style="background:#f7f7f7;padding:12px 14px;margin-bottom:1em;'
            f'border-left:4px solid #333;font-size:0.95em">'
            f"<strong>{LESSON_TITLE}</strong><br>"
            f"{native_lesson}</div>"
        )

    plain = f"""Daily Spanish Verb Practice

Verb: {verb_upper}{cat_note}

{part0_plain}Part 1 — Conjugation

Conjugate this verb for every pronoun in every tense. Write {n_conj} lines (same order as below):

{chr(10).join(lines)}
{part2_plain}

Submit your work to ChatGPT for grading.
"""

    ol_parts = []
    for a in assignments:
        trans = a.get("translation", "")
        if trans:
            ol_parts.append(f"<li>{a['pronoun']} — <strong>{a['tense']}</strong> — {trans}</li>")
        else:
            ol_parts.append(f"<li>{a['pronoun']} — <strong>{a['tense']}</strong></li>")
    ol_items = "".join(ol_parts)

    html = f"""<html><body style="font-family: sans-serif;">
<h2>Daily Spanish Verb Practice</h2>
<p><strong>Verb:</strong> {verb_upper}{cat_note}</p>
{part0_html}
<h3>Part 1 — Conjugation</h3>
<p>Conjugate this verb for every pronoun in every tense. Write {n_conj} lines (same order as below):</p>
<ol>
{ol_items}
</ol>
{part2_html}
<p>Submit your work to ChatGPT for grading.</p>
</body></html>"""

    return plain, html, attach_plain, attach_name


def send_daily_exercise(
    verb: str,
    assignments: list[dict],
    category: str = "",
    track: str = TRACK_IRREGULAR,
    sentences: list[dict] | None = None,
    full_bank_size: int | None = None,
    native_lesson: str | None = None,
    to: str | None = None,
) -> None:
    """Send the daily exercise email to the target address."""
    to = to or TARGET_EMAIL
    if not to:
        raise ValueError("TARGET_EMAIL must be set or pass to=")
    subject = _subject_for_track(verb, track)
    plain, html, att_plain, att_name = build_daily_exercise_body(
        verb,
        assignments,
        category=category,
        sentences=sentences,
        full_bank_size=full_bank_size,
        native_lesson=native_lesson,
    )
    _smtp_send(
        to,
        subject,
        plain,
        html,
        attachment_plain=att_plain,
        attachment_filename=att_name,
    )
