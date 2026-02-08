"""
Daily Spanish Verb Trainer – send daily exercise email.
You get one verb + mixed tenses per day; practice in ChatGPT or however you like.
"""

import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent))

from verb_selector import select_daily_exercise
from email_sender import send_daily_exercise as send_exercise_email


def cmd_send_daily(seed=None) -> None:
    """Pick one verb and random tense per pronoun, send daily exercise email."""
    exercise = select_daily_exercise(seed=seed)
    verb = exercise["verb"]
    assignments = exercise["assignments"]
    send_exercise_email(verb=verb, assignments=assignments)
    print(f"Sent daily exercise: {verb.upper()} (mixed tenses)")


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python main.py send-daily [--seed N]")
        return 1
    cmd = sys.argv[1].lower()
    if cmd == "send-daily":
        seed = None
        if "--seed" in sys.argv:
            i = sys.argv.index("--seed")
            if i + 1 < len(sys.argv):
                try:
                    seed = int(sys.argv[i + 1])
                except ValueError:
                    pass
        cmd_send_daily(seed=seed)
    else:
        print("Usage: python main.py send-daily [--seed N]")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
