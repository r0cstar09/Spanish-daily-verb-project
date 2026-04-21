"""
Pick a rotating slice of sentence prompts for each email (no state file).

Same verb on a different calendar day gets a different window; Pareto vs irregular
track on the same day uses different offsets so the two emails are not identical
when you ever overlap verbs.
"""

from __future__ import annotations

SENTENCES_PER_EMAIL = 10
# Rotate only within the first 100 committed prompts.
ROTATION_BANK_SIZE = 100


def _stable_offset(verb: str, track: str) -> int:
    """Small deterministic offset per (verb, track) pair."""
    h = verb.strip().lower() + "|" + track.strip().lower()
    return sum(ord(c) for c in h) % 997


def rotation_day_key(seed: int | None) -> int:
    """
    Integer that changes per natural day, or follows --seed for reproducible tests.
    When seed is set, use it so the same seed + verb + track always picks the same slice.
    """
    if seed is not None:
        return int(seed) % 100_000
    from datetime import datetime

    return datetime.utcnow().timetuple().tm_yday


def select_sentences_for_email(
    sentences: list[dict],
    *,
    verb: str,
    track: str,
    seed: int | None = None,
    n: int = SENTENCES_PER_EMAIL,
) -> list[dict]:
    """
    Return n sentences (re-numbered id 1..n), wrapping around the bank.
    """
    if not sentences:
        return []
    if len(sentences) > ROTATION_BANK_SIZE:
        sentences = sentences[:ROTATION_BANK_SIZE]
    if len(sentences) <= n:
        out: list[dict] = []
        for i, s in enumerate(sentences):
            row: dict = {"id": i + 1, "en": s["en"]}
            if s.get("sense"):
                row["sense"] = s["sense"]
            if s.get("lesson"):
                row["lesson"] = s["lesson"]
            out.append(row)
        return out

    day_k = rotation_day_key(seed)
    off = _stable_offset(verb, track)
    start = (day_k * 31 + off * 7 + len(sentences)) % len(sentences)

    out: list[dict] = []
    for i in range(n):
        src = sentences[(start + i) % len(sentences)]
        row: dict = {"id": i + 1, "en": src["en"]}
        if src.get("sense"):
            row["sense"] = src["sense"]
        if src.get("lesson"):
            row["lesson"] = src["lesson"]
        out.append(row)
    return out
