"""
Daily Spanish Verb Trainer – verb and tense selection.

Tracks:
  - pareto: high-frequency regular verbs (pareto_regular list).
  - irregular: alternates irregular vs stem_changing (same lists as before).

Each exercise: 5 pronouns × 10 tenses = 50 conjugations.
"""

import json
from datetime import date, datetime
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

IRREGULAR_FOCUS_START_DATE = date(2026, 4, 21)

# Highest-priority irregulars first for faster practical mastery.
IRREGULAR_PRIORITY_ORDER = [
    "ser",
    "haber",
    "ir",
    "estar",
    "tener",
    "hacer",
    "poder",
    "decir",
    "ver",
    "dar",
    "saber",
    "querer",
    "venir",
    "poner",
    "salir",
    "traer",
    "conocer",
    "oír",
    "caer",
    "seguir",
    "elegir",
    "caber",
    "andar",
    "pagar",
    "sacar",
    "conducir",
    "mantener",
    "proponer",
    "satisfacer",
    "freír",
    "reír",
    "huir",
]


def _load_verbs_by_category() -> dict:
    with open(VERBS_BY_CATEGORY_PATH, encoding="utf-8") as f:
        return json.load(f)


def _get_irregular_curriculum_day(seed=None) -> int:
    if seed is not None:
        return max(0, seed)
    day_offset = (datetime.utcnow().date() - IRREGULAR_FOCUS_START_DATE).days
    return max(0, day_offset)


def _get_pareto_verb_index(seed=None, category_size: int = 1) -> int:
    # Hold each regular verb for two consecutive days to allow correction work.
    if seed is not None:
        return (seed // 2) % max(1, category_size)
    day_of_year = datetime.utcnow().timetuple().tm_yday
    return (day_of_year // 2) % max(1, category_size)


def _ordered_irregular_verbs(raw_irregular: list[str]) -> list[str]:
    irregular_set = {v.strip().lower() for v in raw_irregular}
    ordered = [v for v in IRREGULAR_PRIORITY_ORDER if v in irregular_set]
    # Keep any uncategorized leftovers at the end (stable and deterministic).
    leftovers = [v for v in irregular_set if v not in set(ordered)]
    ordered.extend(sorted(leftovers))
    return ordered


def select_daily_exercise(seed=None, track: str = TRACK_IRREGULAR) -> dict:
    """
    Select one verb for the given track.

    track:
      - "pareto" — pareto_regular only, one verb every two days.
      - "irregular" — starts with irregulars (most frequent first), then
        progresses to stem-changing verbs.

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
        irregular_verbs = _ordered_irregular_verbs(data["irregular"])
        stem_verbs = [v.strip().lower() for v in data["stem_changing"]]
        day = _get_irregular_curriculum_day(seed)
        if day < len(irregular_verbs):
            category = "irregular"
            verbs = irregular_verbs
            verb_idx = day
        else:
            category = "stem_changing"
            verbs = stem_verbs
            verb_idx = (day - len(irregular_verbs)) % max(1, len(stem_verbs))
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
