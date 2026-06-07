"""
Daily Spanish Verb Trainer – send daily irregular/stem-changing exercise emails.
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent))

from email_sender import send_daily_exercise as send_exercise_email
from native_lessons import select_native_lesson
from pattern_lesson import build_pattern_lesson
from verb_selector import TRACK_IRREGULAR, select_daily_exercise

DAILY_IRREGULAR_COUNT = 2


def _day_key(seed: int | None) -> int:
    if seed is not None:
        return int(seed) % 100_000
    return datetime.utcnow().timetuple().tm_yday


def cmd_send_daily(seed: int | None = None) -> None:
    sent_verbs: list[str] = []
    for slot in range(DAILY_IRREGULAR_COUNT):
        exercise = select_daily_exercise(
            seed=seed,
            track=TRACK_IRREGULAR,
            slot=slot,
            daily_count=DAILY_IRREGULAR_COUNT,
        )
        verb = exercise["verb"]
        day_key = _day_key(seed)
        native_lesson = select_native_lesson(day_key, TRACK_IRREGULAR)
        pattern_lesson = build_pattern_lesson(verb, day_key=day_key, track=TRACK_IRREGULAR)
        send_exercise_email(
            verb=verb,
            assignments=exercise["assignments"],
            category=exercise.get("category", ""),
            track=TRACK_IRREGULAR,
            pattern_lesson=pattern_lesson,
            native_lesson=native_lesson,
        )
        sent_verbs.append(verb.upper())
    print(f"Sent daily exercise ({TRACK_IRREGULAR}): {', '.join(sent_verbs)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Spanish daily verb trainer")
    sub = parser.add_subparsers(dest="command", required=True)

    p_send = sub.add_parser(
        "send-daily",
        help="Send 2 irregular/stem-changing exercise emails for today",
    )
    p_send.add_argument("--seed", type=int, default=None, help="Override day-based selection (for testing)")

    args = parser.parse_args()
    if args.command == "send-daily":
        cmd_send_daily(seed=args.seed)
    return 0


if __name__ == "__main__":
    sys.exit(main())
