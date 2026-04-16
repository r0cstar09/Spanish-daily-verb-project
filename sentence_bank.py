"""Load per-verb English sentence banks (committed JSON in the repo)."""

import json
from pathlib import Path

SENTENCE_BANKS_DIR = Path(__file__).resolve().parent / "sentence_banks"


def sentence_bank_path(verb: str) -> Path:
    return SENTENCE_BANKS_DIR / f"{verb.strip().lower()}.json"


def load_sentence_bank(verb: str) -> dict:
    """
    Return parsed bank: { "verb", "generated_at", "sentences": [ { "id", "en" }, ... ] }.
    Raises FileNotFoundError or ValueError if missing or empty.
    """
    v = verb.strip().lower()
    path = sentence_bank_path(v)
    if not path.is_file():
        raise FileNotFoundError(
            f"No sentence bank at {path}. Run scripts/build_sentence_banks.py and commit, or add the JSON file."
        )
    with open(path, encoding="utf-8") as f:
        text = f.read()
    # Be tolerant to accidental trailing bytes/objects in committed files:
    # parse the first JSON object and ignore trailing whitespace/data.
    dec = json.JSONDecoder()
    data, _ = dec.raw_decode(text.lstrip())
    sentences = data.get("sentences") or []
    if not sentences:
        raise ValueError(
            f"Sentence bank for {v!r} is empty. Run scripts/build_sentence_banks.py and commit."
        )
    return data
