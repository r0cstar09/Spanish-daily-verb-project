"""
Per-verb usage hints (prepositions, idioms, common patterns).

Used to teach how a verb is actually wielded in real sentences
(e.g. `pensar en`, `acabar de + inf`) without giving conjugated answers.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

USAGE_HINTS_PATH = Path(__file__).resolve().parent / "verb_usage_hints.json"


@lru_cache(maxsize=1)
def _load_usage_hints() -> dict[str, str]:
    with open(USAGE_HINTS_PATH, encoding="utf-8") as f:
        raw = json.load(f)
    return {k.strip().lower(): (v or "").strip() for k, v in raw.items()}


def get_usage_hint(verb: str) -> str:
    """Return a short usage hint for the verb, or an empty string if none."""
    if not verb:
        return ""
    return _load_usage_hints().get(verb.strip().lower(), "")
