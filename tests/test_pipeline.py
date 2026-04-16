"""
Smoke tests: conjugation matrix, sentence banks, rotation, email body assembly.

Does not send email. Does not modify sentence content.
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from email_sender import build_daily_exercise_body  # noqa: E402
from native_lessons import select_native_lesson  # noqa: E402
from sentence_bank import load_sentence_bank  # noqa: E402
from sentence_rotation import (  # noqa: E402
    SENTENCES_PER_EMAIL,
    rotation_day_key,
    select_sentences_for_email,
)
from tenses import TENSES  # noqa: E402
from translations import get_english_translation  # noqa: E402
from verb_selector import (  # noqa: E402
    PRONOUNS,
    TRACK_IRREGULAR,
    TRACK_PARETO,
    select_daily_exercise,
)


def _all_verbs() -> set[str]:
    path = ROOT / "verbs_by_category.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    out: set[str] = set()
    for key in ("pareto_regular", "irregular", "stem_changing"):
        for v in data[key]:
            out.add(v.strip().lower())
    return out


class TestConjugationMatrix(unittest.TestCase):
    def test_tense_and_pronoun_counts(self) -> None:
        self.assertEqual(len(TENSES), 10)
        self.assertEqual(len(PRONOUNS), 5)

    def test_assignment_shape_and_order(self) -> None:
        ex = select_daily_exercise(seed=42, track=TRACK_PARETO)
        assigns = ex["assignments"]
        self.assertEqual(len(assigns), len(TENSES) * len(PRONOUNS))
        i = 0
        for tense in TENSES:
            for pronoun in PRONOUNS:
                row = assigns[i]
                self.assertEqual(row["tense"], tense)
                self.assertEqual(row["pronoun"], pronoun)
                self.assertIn("translation", row)
                i += 1

    def test_translations_match_direct_lookup(self) -> None:
        ex = select_daily_exercise(seed=7, track=TRACK_IRREGULAR)
        verb = ex["verb"]
        for i, row in enumerate(ex["assignments"]):
            pronoun_index = i % len(PRONOUNS)
            tense = row["tense"]
            direct = get_english_translation(verb, pronoun_index, tense)
            self.assertEqual(row["translation"], direct)

    def test_irregular_track_alternates_category_by_seed(self) -> None:
        ex0 = select_daily_exercise(seed=0, track=TRACK_IRREGULAR)
        ex1 = select_daily_exercise(seed=1, track=TRACK_IRREGULAR)
        self.assertNotEqual(ex0["category"], ex1["category"])


class TestSentenceBanksAndRotation(unittest.TestCase):
    def test_every_listed_verb_has_nonempty_bank_json(self) -> None:
        missing: list[str] = []
        empty: list[str] = []
        for v in sorted(_all_verbs()):
            try:
                data = load_sentence_bank(v)
            except (FileNotFoundError, ValueError) as e:
                missing.append(f"{v}: {e}")
                continue
            sents = data.get("sentences") or []
            if not sents:
                empty.append(v)
        self.assertEqual(missing, [], msg="Missing banks:\n" + "\n".join(missing))
        self.assertEqual(empty, [], msg="Empty banks: " + ", ".join(empty))

    def test_rotation_returns_twenty_numbered_prompts(self) -> None:
        ex = select_daily_exercise(seed=99, track=TRACK_PARETO)
        verb = ex["verb"]
        bank = load_sentence_bank(verb)
        full = bank["sentences"]
        picked = select_sentences_for_email(
            full,
            verb=verb,
            track=TRACK_PARETO,
            seed=99,
            n=SENTENCES_PER_EMAIL,
        )
        self.assertEqual(len(picked), SENTENCES_PER_EMAIL)
        for i, row in enumerate(picked, start=1):
            self.assertEqual(row["id"], i)
            self.assertTrue(row.get("en", "").strip())


class TestEmailBody(unittest.TestCase):
    def test_build_includes_conjugation_and_sentence_sections(self) -> None:
        ex = select_daily_exercise(seed=3, track=TRACK_IRREGULAR)
        verb = ex["verb"]
        bank = load_sentence_bank(verb)
        full = bank["sentences"]
        sentences = select_sentences_for_email(
            full,
            verb=verb,
            track=TRACK_IRREGULAR,
            seed=3,
            n=SENTENCES_PER_EMAIL,
        )
        day_key = rotation_day_key(3)
        lesson = select_native_lesson(day_key, TRACK_IRREGULAR)
        plain, html, att_plain, att_name = build_daily_exercise_body(
            verb,
            ex["assignments"],
            category=ex.get("category", ""),
            sentences=sentences,
            full_bank_size=len(full),
            native_lesson=lesson,
        )
        vu = verb.upper()
        self.assertIn(vu, plain)
        self.assertIn("Part 1", plain)
        self.assertIn("Conjugation", plain)
        self.assertIn("Part 2", plain)
        self.assertIn(vu, html)
        self.assertIn("<ol>", html)
        self.assertIn(f"Write {len(ex['assignments'])} lines", plain)
        self.assertTrue(len(plain) > 500)
        self.assertTrue(len(html) > 500)
        if att_plain is not None:
            self.assertIsNotNone(att_name)


class TestMainImport(unittest.TestCase):
    def test_main_module_imports(self) -> None:
        import main  # noqa: F401 — exercise import graph

        self.assertTrue(hasattr(main, "cmd_send_daily"))


if __name__ == "__main__":
    unittest.main()
