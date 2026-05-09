"""
Daily Spanish Verb Trainer – outbound email.
Sends conjugation exercise + sentence-bank practice (evaluate in ChatGPT or elsewhere).
"""

import os
import smtplib
from html import escape
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, make_msgid

from native_lessons import LESSON_TITLE
from verb_selector import TRACK_IRREGULAR, TRACK_PARETO

# Env: SMTP_HOST, SMTP_PORT, EMAIL_USER, EMAIL_PASSWORD, TARGET_EMAIL
def _env(key: str, default: str = "") -> str:
    return (os.environ.get(key) or default).strip()

SMTP_HOST = _env("SMTP_HOST") or "smtp.gmail.com"
SMTP_PORT = int(_env("SMTP_PORT") or "587")
EMAIL_USER = _env("EMAIL_USER")
EMAIL_PASSWORD = _env("EMAIL_PASSWORD")
TARGET_EMAIL = _env("TARGET_EMAIL")

_CATEGORY_LABEL = {
    "pareto_regular": "Pareto (high-frequency regular)",
    "irregular": "irregular",
    "stem_changing": "stem-changing",
}

def _subject_for_track(verb: str, track: str) -> str:
    vu = verb.upper()
    if track == TRACK_PARETO:
        return f"Spanish Verb – Pareto: {vu} (all tenses + sentences)"
    return f"Spanish Verb – Irregular / stem: {vu} (all tenses)"


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
    pattern_lesson: dict | None = None,
    native_lesson: str | None = None,
) -> tuple[str, str, str | None, str | None]:
    """
    Plain and HTML body for pattern-based learning.
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

    lesson = pattern_lesson or {}
    usage = lesson.get("usage_lesson") or {}
    formulas = lesson.get("pattern_formulas") or []
    examples = lesson.get("native_examples") or []
    production = lesson.get("production_drills") or []
    freestyle = lesson.get("freestyle_drills") or []
    repairs = lesson.get("mistake_repair") or []
    repetition = lesson.get("pattern_repetition") or {}

    part2_plain = (
        "\n\nPart 2 — Verb usage lesson\n\n"
        f"{usage.get('core_meaning', '')}\n"
        f"Secondary meanings: {', '.join(usage.get('secondary_meanings', []) or ['(none listed)'])}\n"
        f"Reflexive usage: {' | '.join(usage.get('reflexive_usage', []))}\n"
        f"Non-reflexive usage: {' | '.join(usage.get('non_reflexive_usage', []))}\n"
        f"Common prepositions: {', '.join(usage.get('common_prepositions', []))}\n"
        f"Idiomatic/common chunks: {'; '.join(usage.get('idiomatic_chunks', []))}\n"
        f"Semantic usage patterns: {'; '.join(usage.get('semantic_patterns', []))}\n"
        f"English-speaker traps: {'; '.join(usage.get('english_speaker_traps', []))}\n"
        f"Spanish conceptualization: {usage.get('conceptualization', '')}\n"
    )
    part2_html = (
        "<h3>Part 2 — Verb usage lesson</h3>"
        f"<p>{escape(usage.get('core_meaning', ''))}</p>"
        "<ul>"
        f"<li><strong>Secondary meanings:</strong> {escape(', '.join(usage.get('secondary_meanings', []) or ['(none listed)']))}</li>"
        f"<li><strong>Reflexive usage:</strong> {escape(' | '.join(usage.get('reflexive_usage', [])))}</li>"
        f"<li><strong>Non-reflexive usage:</strong> {escape(' | '.join(usage.get('non_reflexive_usage', [])))}</li>"
        f"<li><strong>Common prepositions:</strong> {escape(', '.join(usage.get('common_prepositions', [])))}</li>"
        f"<li><strong>Idiomatic/common chunks:</strong> {escape('; '.join(usage.get('idiomatic_chunks', [])))}</li>"
        f"<li><strong>Semantic patterns:</strong> {escape('; '.join(usage.get('semantic_patterns', [])))}</li>"
        f"<li><strong>English-speaker traps:</strong> {escape('; '.join(usage.get('english_speaker_traps', [])))}</li>"
        f"<li><strong>Conceptualization:</strong> {escape(usage.get('conceptualization', ''))}</li>"
        "</ul>"
    )

    formula_lines_plain = []
    formula_lines_html = []
    for i, row in enumerate(formulas, start=1):
        formula = row.get("formula", "").strip()
        meaning = row.get("meaning", "").strip()
        formula_lines_plain.append(f"{i}. {formula} = {meaning}")
        formula_lines_html.append(f"<li><code>{escape(formula)}</code> = {escape(meaning)}</li>")
    part3_plain = "\n\nPart 3 — Pattern formulas\n\n" + ("\n".join(formula_lines_plain) if formula_lines_plain else "(none)")
    part3_html = "<h3>Part 3 — Pattern formulas</h3><ol>" + "".join(formula_lines_html) + "</ol>"

    example_lines_plain = []
    example_lines_html = []
    for row in examples:
        i = row.get("id", "")
        es = row.get("es", "").strip()
        en_sem = row.get("en_semantic", "").strip()
        example_lines_plain.append(f"{i}. {es}\n   Meaning: {en_sem}")
        example_lines_html.append(
            f"<li><strong>{escape(str(i))}.</strong> {escape(es)}<br>"
            f"<span style='color:#444'>Meaning: {escape(en_sem)}</span></li>"
        )
    part4_plain = "\n\nPart 4 — Native examples\n\n" + ("\n".join(example_lines_plain) if example_lines_plain else "(none)")
    part4_html = "<h3>Part 4 — Native examples</h3><ol>" + "".join(example_lines_html) + "</ol>"

    prod_lines_plain = []
    prod_lines_html = []
    for row in production:
        i = row.get("id", "")
        prod_lines_plain.append(
            f"Exercise {i}\n"
            f"Pattern: {row.get('pattern', '')}\n"
            f"Meaning to express: {row.get('meaning', '')}\n"
            f"Your Spanish: {row.get('blank', '________________')}\n"
        )
        prod_lines_html.append(
            "<li>"
            f"<strong>Exercise {escape(str(i))}</strong><br>"
            f"Pattern: <code>{escape(row.get('pattern', ''))}</code><br>"
            f"Meaning to express: {escape(row.get('meaning', ''))}<br>"
            f"Your Spanish: {escape(row.get('blank', '________________'))}"
            "</li>"
        )
    part5_plain = "\n\nPart 5 — Pattern production exercises\n\n" + ("\n".join(prod_lines_plain) if prod_lines_plain else "(none)")
    part5_html = "<h3>Part 5 — Pattern production exercises</h3><ol>" + "".join(prod_lines_html) + "</ol>"

    free_lines_plain = []
    free_lines_html = []
    for i, row in enumerate(freestyle, start=1):
        free_lines_plain.append(
            f"Freestyle {i}\n"
            f"Use this pattern: {row.get('pattern', '')}\n"
            f"{row.get('instruction', 'Create 5 original sentences.')}\n"
            f"Vocabulary bias: {row.get('vocab_bias', '')}\n"
        )
        free_lines_html.append(
            "<li>"
            f"Use this pattern: <code>{escape(row.get('pattern', ''))}</code><br>"
            f"{escape(row.get('instruction', 'Create 5 original sentences.'))}<br>"
            f"<span style='color:#444'>Vocabulary bias: {escape(row.get('vocab_bias', ''))}</span>"
            "</li>"
        )
    part6_plain = "\n\nPart 6 — Freestyle drills\n\n" + ("\n".join(free_lines_plain) if free_lines_plain else "(none)")
    part6_html = "<h3>Part 6 — Freestyle drills</h3><ol>" + "".join(free_lines_html) + "</ol>"

    repair_lines_plain = []
    repair_lines_html = []
    for i, row in enumerate(repairs, start=1):
        repair_lines_plain.append(
            f"Mistake {i}\n"
            f"Incorrect Spanish: {row.get('incorrect', '')}\n"
            f"Correction: {row.get('correction', '')}\n"
            f"Why: {row.get('why', '')}\n"
        )
        repair_lines_html.append(
            "<li>"
            f"Incorrect Spanish: {escape(row.get('incorrect', ''))}<br>"
            f"Correction: {escape(row.get('correction', ''))}<br>"
            f"<span style='color:#444'>Why: {escape(row.get('why', ''))}</span>"
            "</li>"
        )
    part7_plain = "\n\nPart 7 — Common mistake repair\n\n" + ("\n".join(repair_lines_plain) if repair_lines_plain else "(none)")
    part7_html = "<h3>Part 7 — Common mistake repair</h3><ol>" + "".join(repair_lines_html) + "</ol>"

    rep_pattern = repetition.get("primary_pattern", "")
    rep_meaning = repetition.get("primary_meaning", "")
    rep_vars = repetition.get("variations", [])
    rep_lines_plain = [f"Primary pattern: {rep_pattern} = {rep_meaning}"]
    rep_lines_html = [f"<p><strong>Primary pattern:</strong> <code>{escape(rep_pattern)}</code> = {escape(rep_meaning)}</p><ol>"]
    for row in rep_vars:
        rep_lines_plain.append(
            f"{row.get('id', '')}. Subject: {row.get('subject', '')} | Tense: {row.get('tense', '')} | "
            f"Context word: {row.get('context_word', '')} | Your Spanish: ____________"
        )
        rep_lines_html.append(
            "<li>"
            f"Subject: {escape(row.get('subject', ''))} | "
            f"Tense: {escape(row.get('tense', ''))} | "
            f"Context word: {escape(row.get('context_word', ''))}<br>"
            "Your Spanish: ____________"
            "</li>"
        )
    rep_lines_html.append("</ol>")
    part8_plain = "\n\nPart 8 — Pattern repetition drill\n\n" + "\n".join(rep_lines_plain)
    part8_html = "<h3>Part 8 — Pattern repetition drill</h3>" + "".join(rep_lines_html)

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
{part2_plain}{part3_plain}{part4_plain}{part5_plain}{part6_plain}{part7_plain}{part8_plain}

Focus on native pattern retrieval instead of direct translation.
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
{part2_html}{part3_html}{part4_html}{part5_html}{part6_html}{part7_html}{part8_html}
<p>Focus on native pattern retrieval instead of direct translation.</p>
</body></html>"""

    return plain, html, None, None


def send_daily_exercise(
    verb: str,
    assignments: list[dict],
    category: str = "",
    track: str = TRACK_IRREGULAR,
    pattern_lesson: dict | None = None,
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
        pattern_lesson=pattern_lesson,
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
