"""
Daily Spanish Verb Trainer – persistent state for daily exercise and reply handling.
Stores today's verb, per-pronoun tense assignments, and whether we've processed a reply.
"""

import json
import os
from datetime import datetime
from pathlib import Path

# In CI (GitHub Actions) set STATE_FILE e.g. to .github/spanish-verb-state.json so state is committed
_state_file = os.environ.get("STATE_FILE")
STATE_PATH = (
    Path(_state_file).resolve()
    if _state_file
    else Path(__file__).resolve().parent / "state.json"
)


def load_state() -> dict | None:
    """Load state from state.json. Returns None if missing or invalid."""
    if not STATE_PATH.exists():
        return None
    try:
        with open(STATE_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def save_state(verb: str, assignments: list[dict], date: str | None = None) -> None:
    """Save today's exercise (verb + pronoun–tense assignments); clear reply_processed_at."""
    if date is None:
        date = datetime.utcnow().strftime("%Y-%m-%d")
    state = {
        "date": date,
        "verb": verb,
        "assignments": assignments,
        "reply_processed_at": None,
    }
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def mark_reply_processed() -> None:
    """Mark that we've processed the reply for the current exercise."""
    state = load_state()
    if not state:
        return
    state["reply_processed_at"] = datetime.utcnow().isoformat() + "Z"
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def get_pending_exercise() -> tuple[str, list[dict]] | None:
    """
    If there is a pending exercise (reply not yet processed), return (verb, assignments).
    Otherwise return None.
    Supports legacy state with single "tense" by converting to one assignment per pronoun.
    """
    state = load_state()
    if not state or state.get("reply_processed_at"):
        return None
    verb = state.get("verb")
    assignments = state.get("assignments")
    if assignments:
        return verb, assignments
    # Legacy: single tense for all
    tense = state.get("tense")
    if verb and tense:
        pronouns = ["yo", "tú", "él / ella", "nosotros / nosotras", "ellos / ellas"]
        return verb, [{"pronoun": p, "tense": tense} for p in pronouns]
    return None


def is_reply_already_processed() -> bool:
    """True if we have already processed a reply for the current exercise."""
    state = load_state()
    return bool(state and state.get("reply_processed_at"))
