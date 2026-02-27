"""
English translations for Spanish verb conjugations.
Generates "I need", "you need", "he/she needs", etc. for each pronoun+tense.
"""

import json
from pathlib import Path

TRANSLATIONS_PATH = Path(__file__).resolve().parent / "verb_translations.json"

PRONOUNS_EN = ["I", "you", "he/she", "we", "they"]
TENSES = ["Present", "Future", "Preterite", "Imperfect", "Conditional"]


def _load_translations() -> dict:
    with open(TRANSLATIONS_PATH, encoding="utf-8") as f:
        return json.load(f)


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


def get_english_translation(verb: str, pronoun_index: int, tense: str) -> str:
    """
    Return English translation for (verb, pronoun, tense).
    pronoun_index: 0=yo, 1=tú, 2=él/ella, 3=nosotros, 4=ellos
    """
    verb = verb.strip().lower()
    trans = _load_translations()
    if verb not in trans:
        return ""
    t = trans[verb]
    pron = PRONOUNS_EN[pronoun_index]

    base = t.get("base", "")
    third = t.get("third") or _get_third_person(base)
    past = t.get("past") or _get_past(base)

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

    return ""


def get_all_translations(verb: str) -> list[str]:
    """Return 25 English translations in assignment order (Present×5, Future×5, ...)."""
    result = []
    for tense in TENSES:
        for p in range(5):
            result.append(get_english_translation(verb, p, tense))
    return result
