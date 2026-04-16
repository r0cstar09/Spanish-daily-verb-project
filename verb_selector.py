"""
Daily Spanish Verb Trainer – verb and tense selection.

Tracks:
  - pareto: high-frequency regular verbs (pareto_regular list).
  - irregular: alternates irregular vs stem_changing (same lists as before).

Each exercise: 5 pronouns × 10 tenses = 50 conjugations.
"""

import json
from datetime import datetime
from pathlib import Path

from tenses import TENSES
from translations import get_english_translation

VERBS_BY_CATEGORY_PATH = Path(__file__).resolve().parent / "verbs_by_category.json"

PRONOUNS = [
    "yo",
    "tú",
    "él / ella",
    "nosotros / nosotras",
    "ellos / ellas",
]

TRACK_PARETO = "pareto"
TRACK_IRREGULAR = "irregular"

IRREGULAR_CATEGORIES = ["irregular", "stem_changing"]
_NUM_IRREGULAR_CATEGORIES = len(IRREGULAR_CATEGORIES)


def _load_verbs_by_category() -> dict:
    with open(VERBS_BY_CATEGORY_PATH, encoding="utf-8") as f:
        return json.load(f)


def _get_irregular_category_index(seed=None) -> int:
    if seed is not None:
        return seed % _NUM_IRREGULAR_CATEGORIES
    day_of_year = datetime.utcnow().timetuple().tm_yday
    return day_of_year % _NUM_IRREGULAR_CATEGORIES


def _get_irregular_verb_index(seed=None, category_size: int = 1) -> int:
    if seed is not None:
        return (seed // _NUM_IRREGULAR_CATEGORIES) % max(1, category_size)
    day_of_year = datetime.utcnow().timetuple().tm_yday
    return (day_of_year // _NUM_IRREGULAR_CATEGORIES) % max(1, category_size)


def _get_pareto_verb_index(seed=None, category_size: int = 1) -> int:
    if seed is not None:
        return seed % max(1, category_size)
    day_of_year = datetime.utcnow().timetuple().tm_yday
    return day_of_year % max(1, category_size)


def select_daily_exercise(seed=None, track: str = TRACK_IRREGULAR) -> dict:
    """
    Select one verb for the given track.

    track:
      - "pareto" — pareto_regular only (independent day index from irregular track).
      - "irregular" — alternates irregular / stem_changing.

    Returns assignments: 5 pronouns × 10 tenses = 50 conjugations with English translations.
    """
    track = (track or TRACK_IRREGULAR).strip().lower()
    data = _load_verbs_by_category()

    if track == TRACK_PARETO:
        verbs = [v.strip().lower() for v in data["pareto_regular"]]
        verb_idx = _get_pareto_verb_index(seed, len(verbs))
        verb = verbs[verb_idx]
        category = "pareto_regular"
    elif track == TRACK_IRREGULAR:
        cat_idx = _get_irregular_category_index(seed)
        category = IRREGULAR_CATEGORIES[cat_idx]
        verbs = [v.strip().lower() for v in data[category]]
        verb_idx = _get_irregular_verb_index(seed, len(verbs))
        verb = verbs[verb_idx]
    else:
        raise ValueError(
            f"Unknown track {track!r}. Use {TRACK_PARETO!r} or {TRACK_IRREGULAR!r}."
        )

    assignments = []
    for t in TENSES:
        for i, p in enumerate(PRONOUNS):
            translation = get_english_translation(verb, i, t)
            assignments.append({"pronoun": p, "tense": t, "translation": translation})

    return {
        "verb": verb,
        "assignments": assignments,
        "category": category,
        "track": track,
    }


if __name__ == "__main__":
    for tr in (TRACK_PARETO, TRACK_IRREGULAR):
        ex = select_daily_exercise(track=tr)
        print(f"Track {tr}: {ex['verb'].upper()} (category: {ex['category']})")
