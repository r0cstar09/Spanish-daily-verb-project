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

# Reset both tracks from this date.
CURRICULUM_RESET_DATE = date(2026, 5, 20)

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


def _get_irregular_curriculum_day(seed=None, *, slot: int = 0, daily_count: int = 1) -> int:
    slot = max(0, int(slot))
    daily_count = max(1, int(daily_count))
    if seed is not None:
        return max(0, seed) * daily_count + slot
    day_offset = (datetime.utcnow().date() - CURRICULUM_RESET_DATE).days
    return max(0, day_offset) * daily_count + slot


def _get_pareto_curriculum_day(seed=None) -> int:
    if seed is not None:
        return max(0, seed)
    day_offset = (datetime.utcnow().date() - CURRICULUM_RESET_DATE).days
    return max(0, day_offset)


def _ending_buckets(verbs: list[str]) -> dict[str, list[str]]:
    buckets = {"ar": [], "er": [], "ir": []}
    for v in verbs:
        vv = v.strip().lower()
        for ending in ("ar", "er", "ir"):
            if vv.endswith(ending):
                buckets[ending].append(vv)
                break
    return buckets


def _ordered_irregular_verbs(raw_irregular: list[str]) -> list[str]:
    irregular_set = {v.strip().lower() for v in raw_irregular}
    ordered = [v for v in IRREGULAR_PRIORITY_ORDER if v in irregular_set]
    # Keep any uncategorized leftovers at the end (stable and deterministic).
    leftovers = [v for v in irregular_set if v not in set(ordered)]
    ordered.extend(sorted(leftovers))
    return ordered


def select_daily_exercise(
    seed=None,
    track: str = TRACK_IRREGULAR,
    *,
    slot: int = 0,
    daily_count: int = 1,
) -> dict:
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
        buckets = _ending_buckets(verbs)
        cycle_order = ("ir", "er", "ar")
        day = _get_pareto_curriculum_day(seed)
        ending = cycle_order[day % len(cycle_order)]
        ending_list = buckets[ending]
        if not ending_list:
            raise ValueError(f"No Pareto verbs found for ending '{ending}'.")
        verb_idx = (day // len(cycle_order)) % len(ending_list)
        verb = ending_list[verb_idx]
        category = "pareto_regular"
    elif track == TRACK_IRREGULAR:
        irregular_verbs = _ordered_irregular_verbs(data["irregular"])
        stem_verbs = [v.strip().lower() for v in data["stem_changing"]]
        day = _get_irregular_curriculum_day(seed, slot=slot, daily_count=daily_count)
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
