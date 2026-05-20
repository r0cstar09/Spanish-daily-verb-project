"""
Daily Spanish Verb Trainer – send daily exercise email (Pareto or irregular/stem track).
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
from verb_selector import TRACK_IRREGULAR, TRACK_PARETO, select_daily_exercise


def _day_key(seed: int | None) -> int:
    if seed is not None:
        return int(seed) % 100_000
    return datetime.utcnow().timetuple().tm_yday


def cmd_send_daily(track: str, seed: int | None = None) -> None:
    # Daily target: 1 regular (pareto) and 2 irregular/stem exercises.
    daily_count = 2 if track == TRACK_IRREGULAR else 1
    sent_verbs: list[str] = []
    for slot in range(daily_count):
        exercise = select_daily_exercise(
            seed=seed,
            track=track,
            slot=slot,
            daily_count=daily_count,
        )
        verb = exercise["verb"]
        day_key = _day_key(seed)
        native_lesson = select_native_lesson(day_key, track)
        pattern_lesson = build_pattern_lesson(verb, day_key=day_key, track=track)
        send_exercise_email(
            verb=verb,
            assignments=exercise["assignments"],
            category=exercise.get("category", ""),
            track=track,
            pattern_lesson=pattern_lesson,
            native_lesson=native_lesson,
        )
        sent_verbs.append(verb.upper())
    print(f"Sent daily exercise ({track}): {', '.join(sent_verbs)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Spanish daily verb trainer")
    sub = parser.add_subparsers(dest="command", required=True)

    p_send = sub.add_parser("send-daily", help="Send one exercise email for the given track")
    p_send.add_argument(
        "--track",
        choices=[TRACK_PARETO, TRACK_IRREGULAR],
        required=True,
        help=f"{TRACK_PARETO!r}: high-frequency regulars; {TRACK_IRREGULAR!r}: irregular / stem-changing (alternating)",
    )
    p_send.add_argument("--seed", type=int, default=None, help="Override day-based selection (for testing)")

    args = parser.parse_args()
    if args.command == "send-daily":
        cmd_send_daily(track=args.track, seed=args.seed)
    return 0


if __name__ == "__main__":
    sys.exit(main())
