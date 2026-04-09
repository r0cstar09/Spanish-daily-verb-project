"""
Daily Spanish Verb Trainer – verb and tense selection.
Picks one verb per day from irregular or stem-changing verbs only.
Tests every pronoun (yo, tú, él/ella, nosotros, ellos) in eight forms:
Present, Future, Preterite, Imperfect, Conditional, Present Perfect, Present Subjunctive, Estar + Gerund — 40 conjugations total.

Alternates between irregular and stem_changing (by day of year).
"""

import json
from datetime import datetime
from pathlib import Path

from translations import get_english_translation

VERBS_BY_CATEGORY_PATH = Path(__file__).resolve().parent / "verbs_by_category.json"
TENSES = [
    "Present", "Future", "Preterite", "Imperfect", "Conditional",
    "Present Perfect", "Present Subjunctive", "Estar + Gerund",
]
PRONOUNS = [
    "yo",
    "tú",
    "él / ella",
    "nosotros / nosotras",
    "ellos / ellas",
]

# Only irregular and stem-changing verbs
CATEGORIES = ["irregular", "stem_changing"]
_NUM_CATEGORIES = len(CATEGORIES)


def _load_verbs_by_category() -> dict:
    with open(VERBS_BY_CATEGORY_PATH, encoding="utf-8") as f:
        return json.load(f)


def _get_category_index(seed=None) -> int:
    """Return 0 (irregular) or 1 (stem_changing). Uses day of year when no seed, else seed."""
    if seed is not None:
        return seed % _NUM_CATEGORIES
    day_of_year = datetime.utcnow().timetuple().tm_yday
    return day_of_year % _NUM_CATEGORIES


def _get_verb_index_in_category(seed=None, category_size: int = 1) -> int:
    """Return index within the category. Uses day of year when no seed, else seed."""
    if seed is not None:
        return (seed // _NUM_CATEGORIES) % max(1, category_size)
    day_of_year = datetime.utcnow().timetuple().tm_yday
    return (day_of_year // _NUM_CATEGORIES) % max(1, category_size)


def select_daily_exercise(seed=None) -> dict:
    """
    Select one verb from irregular or stem_changing (alternates daily).
    Returns assignments: all 5 pronouns × 8 forms = 40 conjugations with English translations.
    """
    data = _load_verbs_by_category()
    cat_idx = _get_category_index(seed)
    category = CATEGORIES[cat_idx]
    verbs = [v.strip().lower() for v in data[category]]
    verb_idx = _get_verb_index_in_category(seed, len(verbs))
    verb = verbs[verb_idx]

    assignments = []
    for t in TENSES:
        for i, p in enumerate(PRONOUNS):
            translation = get_english_translation(verb, i, t)
            assignments.append({"pronoun": p, "tense": t, "translation": translation})

    return {
        "verb": verb,
        "assignments": assignments,
        "category": category,
    }


if __name__ == "__main__":
    ex = select_daily_exercise()
    print(f"Verb: {ex['verb'].upper()} (category: {ex['category']})")
    print("Assignments:")
    for a in ex["assignments"][:5]:
        print(f"  {a['pronoun']} → {a['tense']} — {a.get('translation', '')}")
