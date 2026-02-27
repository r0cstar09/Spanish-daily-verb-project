"""
Daily Spanish Verb Trainer – verb and tense selection.
Picks one verb per day. Tests every pronoun (yo, tú, él/ella, nosotros, ellos) in all five tenses:
Present, Future, Preterite, Imperfect, Conditional — 25 conjugations total.
"""

import json
import random
from pathlib import Path

from translations import get_english_translation

VERBS_PATH = Path(__file__).resolve().parent / "verbs.json"
TENSES = ["Present", "Future", "Preterite", "Imperfect", "Conditional"]
PRONOUNS = [
    "yo",
    "tú",
    "él / ella",
    "nosotros / nosotras",
    "ellos / ellas",
]


def load_verbs() -> list[str]:
    """Load verb list from verbs.json."""
    with open(VERBS_PATH, encoding="utf-8") as f:
        return json.load(f)


def select_daily_exercise(seed=None) -> dict:
    """
    Select one verb. Returns assignments: all 5 pronouns × 5 tenses = 25 conjugations.
    Order: Present (all pronouns), Future (all), Preterite (all), Imperfect (all), Conditional (all).
    """
    if seed is not None:
        random.seed(seed)
    verbs = load_verbs()
    verb = random.choice(verbs).strip().lower()
    assignments = []
    for t in TENSES:
        for i, p in enumerate(PRONOUNS):
            translation = get_english_translation(verb, i, t)
            assignments.append({"pronoun": p, "tense": t, "translation": translation})
    return {
        "verb": verb,
        "assignments": assignments,
    }


if __name__ == "__main__":
    ex = select_daily_exercise()
    print(f"Verb: {ex['verb'].upper()}")
    print("Assignments:")
    for a in ex["assignments"]:
        print(f"  {a['pronoun']} → {a['tense']}")
