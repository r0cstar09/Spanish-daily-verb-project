"""
Daily Spanish Verb Trainer – verb and tense selection.
Picks one verb per day and assigns a random tense to each pronoun (mixed tenses).
"""

import json
import random
from pathlib import Path

VERBS_PATH = Path(__file__).resolve().parent / "verbs.json"
TENSES = ["Present", "Preterite", "Imperfect", "Future"]
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
    Select one verb and, for each pronoun, a random tense.
    Returns dict with keys: verb, assignments (list of {pronoun, tense}).
    """
    if seed is not None:
        random.seed(seed)
    verbs = load_verbs()
    verb = random.choice(verbs).strip().lower()
    assignments = [
        {"pronoun": p, "tense": random.choice(TENSES)}
        for p in PRONOUNS
    ]
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
