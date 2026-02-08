"""
Daily Spanish Verb Trainer – LLM evaluation of user sentences.
Corrects grammar per pronoun+tense, explains mistakes, returns conjugation tables and rewritten sentences.
"""

import json
import os
import re

# Use OpenAI by default; set OPENAI_API_KEY
OPENAI_API_KEY = (os.environ.get("OPENAI_API_KEY") or "").strip()
LLM_MODEL = (os.environ.get("LLM_MODEL") or "gpt-4o-mini").strip()


def _build_evaluation_prompt(
    verb: str,
    assignments: list[dict],
    user_sentences: list[str],
) -> str:
    """Build the prompt sent to the LLM for evaluation (mixed tenses per pronoun)."""
    lines = [
        f"{i+1}. {a['pronoun']} — tense: {a['tense']}"
        for i, a in enumerate(assignments)
    ]
    assignments_block = "\n".join(lines)
    sentences_block = "\n".join(f"{i+1}. {s}" for i, s in enumerate(user_sentences))
    return f"""You are a strict but kind Spanish teacher. Evaluate the following student sentences.

Verb (infinitive): {verb}

Expected (pronoun and tense for each line, in order):
{assignments_block}

Student's sentences (one per line, in order):
{sentences_block}

Respond with a valid JSON object only, no markdown or extra text. Use this exact structure:

{{
  "results": [
    {{
      "pronoun": "yo",
      "tense": "Future",
      "original": "exact student sentence",
      "correct": true or false,
      "corrected": "corrected sentence if wrong, otherwise same as original",
      "explanation": "brief explanation in simple English if wrong; if correct write 'Correct.'"
    }}
  ],
  "conjugation_tables": {{
    "Future": "yo [form]\\ntú [form]\\nél/ella [form]\\nnosotros/nosotras [form]\\nellos/ellas [form]",
    "Preterite": "...",
    "Imperfect": "...",
    "Present": "..."
  }},
  "encouragement": "One short sentence of encouragement or a pattern reminder."
}}

Rules:
- Evaluate strictly: each sentence must match the requested tense AND pronoun for that line.
- Output one entry in "results" per line, in the same order. Include "pronoun" and "tense" in each entry.
- In "conjugation_tables", include ONLY the tenses that appear in the assignments above (one key per tense used). Each value is 5 lines: yo ..., tú ..., él/ella ..., nosotros/nosotras ..., ellos/ellas ...
- If the student gave fewer than 5 sentences, still output 5 entries; use "original": "(missing)" and "correct": false for missing ones, and suggest a correct example in "corrected".
- Keep explanations very brief (one line).
- Output only the JSON object."""


def _call_openai(prompt: str) -> str:
    """Call OpenAI API and return assistant content."""
    try:
        import openai
    except ImportError:
        raise ImportError("Install openai: pip install openai")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY must be set")
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content or ""


def _parse_llm_response(raw: str) -> dict:
    """Parse LLM response into structured dict. Tolerate markdown code blocks."""
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```\s*$", "", text)
    return json.loads(text)


def evaluate(
    verb: str,
    assignments: list[dict],
    user_sentences: list[str],
) -> dict:
    """
    Evaluate user sentences with the LLM (one tense per pronoun).
    Returns dict with: results, conjugation_tables (dict tense -> table str), encouragement.
    """
    prompt = _build_evaluation_prompt(verb, assignments, user_sentences)
    raw = _call_openai(prompt)
    data = _parse_llm_response(raw)
    results = data.get("results", [])
    conjugation_tables = data.get("conjugation_tables", {})
    if isinstance(conjugation_tables, list):
        conjugation_tables = {}
    encouragement = data.get("encouragement", "Keep practicing!")
    return {
        "results": results,
        "conjugation_tables": conjugation_tables,
        "encouragement": encouragement,
    }


def format_corrected_sections(results: list[dict]) -> list[str]:
    """Turn LLM results into the list of text sections for the feedback email (include tense)."""
    sections = []
    for r in results:
        pronoun = r.get("pronoun", "?")
        tense = r.get("tense", "")
        label = f"{pronoun}" + (f" ({tense})" if tense else "")
        original = r.get("original", "")
        correct = r.get("correct", False)
        corrected = r.get("corrected", original)
        explanation = r.get("explanation", "")
        if correct:
            sections.append(
                f"Your sentence ({label}):\n{original}\n\n✔ Correct."
            )
        else:
            sections.append(
                f"Your sentence ({label}):\n{original}\n\n"
                f"Correction:\n{corrected}\n\n"
                f"Why:\n{explanation}"
            )
    return sections


def format_conjugation_tables(conjugation_tables: dict) -> str:
    """Format conjugation_tables dict as one string for the feedback email."""
    if not conjugation_tables:
        return "(No tables returned)"
    parts = []
    for tense, table in conjugation_tables.items():
        if table and table.strip():
            parts.append(f"--- {tense} ---\n{table.strip()}")
    return "\n\n".join(parts) if parts else "(No tables returned)"


def get_sample_prompt() -> str:
    """Return sample evaluation prompt for documentation (mixed tenses)."""
    return _build_evaluation_prompt(
        verb="llevar",
        assignments=[
            {"pronoun": "yo", "tense": "Future"},
            {"pronoun": "tú", "tense": "Imperfect"},
            {"pronoun": "él / ella", "tense": "Present"},
            {"pronoun": "nosotros / nosotras", "tense": "Preterite"},
            {"pronoun": "ellos / ellas", "tense": "Future"},
        ],
        user_sentences=[
            "Yo llevaré el libro.",
            "Tú llevabas el bolso.",
            "Ella lleva la maleta.",
            "Nosotros llevamos las cajas.",
            "Ellos llevarán el equipaje.",
        ],
    )
