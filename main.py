"""
Daily Spanish Verb Trainer – send daily exercise email (Pareto or irregular/stem track).
"""

import argparse
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent))

from email_sender import send_daily_exercise as send_exercise_email
from native_lessons import select_native_lesson
from sentence_bank import load_sentence_bank
from sentence_rotation import (
    ROTATION_BANK_SIZE,
    SENTENCES_PER_EMAIL,
    rotation_day_key,
    select_sentences_for_email,
)
from verb_selector import TRACK_IRREGULAR, TRACK_PARETO, select_daily_exercise


def cmd_send_daily(track: str, seed: int | None = None) -> None:
    exercise = select_daily_exercise(seed=seed, track=track)
    verb = exercise["verb"]
    bank = load_sentence_bank(verb)
    full_bank = bank["sentences"][:ROTATION_BANK_SIZE]
    sentences = select_sentences_for_email(
        full_bank,
        verb=verb,
        track=track,
        seed=seed,
        n=SENTENCES_PER_EMAIL,
    )
    day_key = rotation_day_key(seed)
    native_lesson = select_native_lesson(day_key, track)
    send_exercise_email(
        verb=verb,
        assignments=exercise["assignments"],
        category=exercise.get("category", ""),
        track=track,
        sentences=sentences,
        full_bank_size=len(full_bank),
        native_lesson=native_lesson,
    )
    n = len(exercise["assignments"])
    print(
        f"Sent daily exercise ({track}): {verb.upper()} "
        f"({n} conjugations + {len(sentences)} sentence prompts, bank has {len(full_bank)})"
    )


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
