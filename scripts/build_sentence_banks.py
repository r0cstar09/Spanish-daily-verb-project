#!/usr/bin/env python3
"""
Validate committed sentence banks.

This project now reads sentence prompts directly from committed JSON files in
sentence_banks/. This script does not generate sentence text.

Usage:
  python scripts/build_sentence_banks.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERBS_PATH = ROOT / "verbs_by_category.json"
BANKS_DIR = ROOT / "sentence_banks"

import sys

sys.path.insert(0, str(ROOT))

from sentence_bank import load_sentence_bank  # noqa: E402

def all_verbs() -> list[str]:
    with open(VERBS_PATH, encoding="utf-8") as f:
        data = json.load(f)
    seen: set[str] = set()
    for key in ("pareto_regular", "irregular", "stem_changing"):
        for v in data[key]:
            seen.add(v.strip().lower())
    return sorted(seen)


def _validate_bank(verb: str) -> None:
    path = BANKS_DIR / f"{verb}.json"
    if not path.is_file():
        raise FileNotFoundError(f"Missing bank file: {path.relative_to(ROOT)}")
    payload = load_sentence_bank(verb)
    if payload.get("verb") != verb:
        got = payload.get("verb")
        raise ValueError(f"{path.relative_to(ROOT)}: 'verb' mismatch (expected {verb!r}, got {got!r})")
    sentences = payload.get("sentences")
    if not isinstance(sentences, list) or not sentences:
        raise ValueError(f"{path.relative_to(ROOT)}: 'sentences' must be a non-empty list")
    if len(sentences) < 20:
        raise ValueError(f"{path.relative_to(ROOT)}: expected at least 20 sentences, got {len(sentences)}")
    for i, row in enumerate(sentences, start=1):
        if not isinstance(row, dict):
            raise ValueError(f"{path.relative_to(ROOT)}: sentence #{i} is not an object")
        en = (row.get("en") or "").strip()
        if not en:
            raise ValueError(f"{path.relative_to(ROOT)}: sentence #{i} has empty 'en'")


def main() -> int:
    verbs = all_verbs()
    errors: list[str] = []
    for verb in verbs:
        try:
            _validate_bank(verb)
        except Exception as e:  # noqa: BLE001
            errors.append(str(e))
    if errors:
        print("Sentence bank validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1
    print(f"Validated {len(verbs)} sentence bank JSON files in sentence_banks/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
