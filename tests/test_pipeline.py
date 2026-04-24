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
from verb_usage import get_usage_hint  # noqa: E402
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


def _all_sentence_bank_verbs() -> set[str]:
    return {path.stem.strip().lower() for path in (ROOT / "sentence_banks").glob("*.json")}


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

    def test_pareto_track_repeats_same_verb_for_two_days(self) -> None:
        ex0 = select_daily_exercise(seed=0, track=TRACK_PARETO)
        ex1 = select_daily_exercise(seed=1, track=TRACK_PARETO)
        ex2 = select_daily_exercise(seed=2, track=TRACK_PARETO)
        self.assertEqual(ex0["verb"], ex1["verb"])
        self.assertNotEqual(ex1["verb"], ex2["verb"])

    def test_translations_match_direct_lookup(self) -> None:
        ex = select_daily_exercise(seed=7, track=TRACK_IRREGULAR)
        verb = ex["verb"]
        for i, row in enumerate(ex["assignments"]):
            pronoun_index = i % len(PRONOUNS)
            tense = row["tense"]
            direct = get_english_translation(verb, pronoun_index, tense)
            self.assertEqual(row["translation"], direct)

    def test_irregular_track_starts_with_irregulars(self) -> None:
        ex0 = select_daily_exercise(seed=0, track=TRACK_IRREGULAR)
        ex1 = select_daily_exercise(seed=1, track=TRACK_IRREGULAR)
        self.assertEqual(ex0["category"], "irregular")
        self.assertEqual(ex1["category"], "irregular")

    def test_irregular_track_moves_to_stem_changing_after_irregular_block(self) -> None:
        path = ROOT / "verbs_by_category.json"
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        irregular_count = len(data["irregular"])
        ex = select_daily_exercise(seed=irregular_count, track=TRACK_IRREGULAR)
        self.assertEqual(ex["category"], "stem_changing")


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

    def test_rotation_returns_numbered_prompts_for_daily_limit(self) -> None:
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
    def test_irregular_build_includes_only_conjugation_section(self) -> None:
        ex = select_daily_exercise(seed=3, track=TRACK_IRREGULAR)
        verb = ex["verb"]
        day_key = rotation_day_key(3)
        lesson = select_native_lesson(day_key, TRACK_IRREGULAR)
        plain, html, att_plain, att_name = build_daily_exercise_body(
            verb,
            ex["assignments"],
            category=ex.get("category", ""),
            sentences=[],
            full_bank_size=0,
            native_lesson=lesson,
        )
        vu = verb.upper()
        self.assertIn(vu, plain)
        self.assertIn("Part 1", plain)
        self.assertIn("Conjugation", plain)
        self.assertNotIn("Part 2", plain)
        self.assertIn(vu, html)
        self.assertIn("<ol>", html)
        self.assertIn(f"Write {len(ex['assignments'])} lines", plain)
        self.assertTrue(len(plain) > 300)
        self.assertTrue(len(html) > 300)
        self.assertIsNone(att_plain)
        self.assertIsNone(att_name)

class TestUsageHints(unittest.TestCase):
    def test_every_listed_verb_has_usage_hint(self) -> None:
        missing = [v for v in sorted(_all_verbs()) if not get_usage_hint(v)]
        self.assertEqual(missing, [], msg="Verbs missing usage hint: " + ", ".join(missing))

    def test_every_sentence_bank_verb_has_usage_hint(self) -> None:
        missing = [v for v in sorted(_all_sentence_bank_verbs()) if not get_usage_hint(v)]
        self.assertEqual(missing, [], msg="Sentence-bank verbs missing usage hint: " + ", ".join(missing))

    def test_usage_hint_rendered_in_email_body(self) -> None:
        ex = select_daily_exercise(seed=0, track=TRACK_IRREGULAR)
        verb = ex["verb"]
        expected = get_usage_hint(verb)
        self.assertTrue(expected, f"No usage hint found for {verb!r}")
        plain, html, _a, _b = build_daily_exercise_body(
            verb,
            ex["assignments"],
            category=ex.get("category", ""),
            sentences=[],
            full_bank_size=0,
            native_lesson=None,
        )
        self.assertIn("Construction hints (prepositions/patterns):", plain)
        self.assertIn(expected, plain)
        self.assertIn("Construction hints (prepositions/patterns):", html)
        self.assertIn(expected, html)


class TestMainImport(unittest.TestCase):
    def test_main_module_imports(self) -> None:
        import main  # noqa: F401 — exercise import graph

        self.assertTrue(hasattr(main, "cmd_send_daily"))


if __name__ == "__main__":
    unittest.main()
