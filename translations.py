"""
English translations for Spanish verb conjugations.
Uses verb_translations.json; falls back to pareto_glosses.json for Pareto verbs.
"""

import json
from pathlib import Path

TRANSLATIONS_PATH = Path(__file__).resolve().parent / "verb_translations.json"
GLOSSES_PATH = Path(__file__).resolve().parent / "pareto_glosses.json"

PRONOUNS_EN = ["I", "you", "he/she", "we", "they"]

# Imperfect subjunctive English cues (if X were to + infinitive)
_IF_WERE_TO = [
    "if I were to",
    "if you were to",
    "if he/she were to",
    "if we were to",
    "if they were to",
]


def _load_translations() -> dict:
    with open(TRANSLATIONS_PATH, encoding="utf-8") as f:
        return json.load(f)


def _load_glosses() -> dict:
    if not GLOSSES_PATH.is_file():
        return {}
    with open(GLOSSES_PATH, encoding="utf-8") as f:
        return json.load(f)


def _resolve_entry(verb: str) -> dict | None:
    verb = verb.strip().lower()
    trans = _load_translations()
    if verb in trans:
        return trans[verb]
    glosses = _load_glosses()
    if verb in glosses:
        g = glosses[verb]
        if isinstance(g, str):
            return {"base": g}
        return g
    return None


def get_english_base(verb: str) -> str:
    """Bare English verb stem (e.g. speak) for offline sentence-bank templates."""
    t = _resolve_entry(verb.strip().lower())
    if t is None:
        return ""
    return (t.get("base") or "").strip()


def _get_third_person(base: str) -> str:
    """Derive third person singular from base (e.g. need -> needs)."""
    if base.endswith(("s", "x", "z", "ch", "sh")):
        return base + "es"
    return base + "s"


def _get_past(base: str) -> str:
    """Derive past form from base (e.g. need -> needed). Fallback for missing irregulars."""
    if base.endswith("e"):
        return base + "d"
    if base.endswith("y") and base[-2] not in "aeiou":
        return base[:-1] + "ied"
    return base + "ed"


def _get_present_participle(base: str) -> str:
    """Derive -ing form (e.g. need -> needing)."""
    if base.endswith("e"):
        return base[:-1] + "ing"
    if len(base) >= 3 and base[-1] in "bdfgmnprt" and base[-2] in "aeiou" and base[-3] not in "aeiou":
        return base + base[-1] + "ing"  # run -> running
    return base + "ing"


def get_english_translation(verb: str, pronoun_index: int, tense: str) -> str:
    """
    Return English translation for (verb, pronoun, tense).
    pronoun_index: 0=yo, 1=tú, 2=él/ella, 3=nosotros, 4=ellos
    """
    t = _resolve_entry(verb)
    if t is None:
        return ""
    pron = PRONOUNS_EN[pronoun_index]

    base = t.get("base", "")
    third = t.get("third") or _get_third_person(base)
    past = t.get("past") or _get_past(base)
    pp = t.get("pp") or past  # past participle
    gerund = t.get("gerund") or _get_present_participle(base)

    if tense == "Present":
        if "present_forms" in t:
            return f"{pron} {t['present_forms'][pronoun_index]}"
        if pronoun_index == 2:
            return f"{pron} {third}"
        return f"{pron} {base}"

    if tense == "Future":
        phrase = t.get("future") or f"will {base}"
        return f"{pron} {phrase}"

    if tense == "Preterite":
        if "past_forms" in t:
            return f"{pron} {t['past_forms'][pronoun_index]}"
        return f"{pron} {past}"

    if tense == "Imperfect":
        phrase = t.get("imperfect") or f"used to {base}"
        return f"{pron} {phrase}"

    if tense == "Conditional":
        phrase = t.get("conditional") or f"would {base}"
        return f"{pron} {phrase}"

    if tense == "Present Perfect":
        return f"{pron} have {pp}" if pronoun_index in (0, 1, 3, 4) else f"{pron} has {pp}"

    if tense == "Pluperfect":
        return f"{pron} had {pp}"

    if tense == "Present Subjunctive":
        return f"that {pron} {base}"

    if tense == "Imperfect Subjunctive":
        return f"{_IF_WERE_TO[pronoun_index]} {base}"

    if tense == "Estar + Gerund":
        estar_forms = ["am", "are", "is", "are", "are"]
        return f"{pron} {estar_forms[pronoun_index]} {gerund}"

    return ""
