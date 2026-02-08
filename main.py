"""
Daily Spanish Verb Trainer – main entry point.
Run with: send-daily | check-replies
- send-daily: pick verb+tense, send exercise email, save state.
- check-replies: fetch replies, evaluate with LLM, send feedback email.
"""

import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent / ".env")
except ImportError:
    pass

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from verb_selector import select_daily_exercise
from email_sender import send_daily_exercise as send_exercise_email, send_feedback
from email_reader import fetch_replies
from llm_evaluator import evaluate, format_corrected_sections, format_conjugation_tables
from state import (
    save_state,
    get_pending_exercise,
    mark_reply_processed,
    is_reply_already_processed,
)


def cmd_send_daily(seed=None) -> None:
    """Select one verb and random tense per pronoun, save state, send daily exercise email."""
    exercise = select_daily_exercise(seed=seed)
    verb = exercise["verb"]
    assignments = exercise["assignments"]
    save_state(verb=verb, assignments=assignments)
    send_exercise_email(verb=verb, assignments=assignments)
    print(f"Sent daily exercise: {verb.upper()} (mixed tenses)")


def cmd_check_replies() -> None:
    """Fetch replies, evaluate with LLM, send feedback; process at most one reply per run."""
    pending = get_pending_exercise()
    if not pending:
        if is_reply_already_processed():
            print("Reply for today's exercise already processed. Nothing to do.")
        else:
            print("No pending exercise (run send-daily first).")
        return
    verb, assignments = pending
    replies = fetch_replies(limit=5)
    if not replies:
        print("No replies found. Reply to the daily exercise email with your 5 sentences.")
        return
    reply = replies[0]
    sentences = reply.get("sentences", [])
    if not sentences:
        print("Reply had no extractable sentences. Reply with 5 lines (one per pronoun).")
        return
    print(f"Evaluating {len(sentences)} sentences for {verb} (mixed tenses)...")
    result = evaluate(verb=verb, assignments=assignments, user_sentences=sentences)
    sections = format_corrected_sections(result["results"])
    conjugation_tables_str = format_conjugation_tables(result["conjugation_tables"])
    send_feedback(
        verb=verb,
        corrected_sections=sections,
        conjugation_tables=conjugation_tables_str,
        encouragement=result["encouragement"],
    )
    mark_reply_processed()
    print("Feedback email sent.")


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python main.py send-daily [--seed N] | python main.py check-replies")
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
    elif cmd == "check-replies":
        cmd_check_replies()
    else:
        print("Usage: python main.py send-daily [--seed N] | python main.py check-replies")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
