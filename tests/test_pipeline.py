"""Smoke tests for the pattern-based daily lesson pipeline."""

from __future__ import annotations

import json
import sys
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from email_sender import build_daily_exercise_body  # noqa: E402
from native_lessons import select_native_lesson  # noqa: E402
from pattern_lesson import build_pattern_lesson  # noqa: E402
from tenses import TENSES  # noqa: E402
from translations import get_english_translation  # noqa: E402
from verb_selector import (  # noqa: E402
    PRONOUNS,
    TRACK_IRREGULAR,
    TRACK_PARETO,
    select_daily_exercise,
)


def _day_key(seed: int | None) -> int:
    if seed is not None:
        return int(seed) % 100_000
    return datetime.utcnow().timetuple().tm_yday


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


class TestPatternLesson(unittest.TestCase):
    def test_pattern_lesson_has_required_sections(self) -> None:
        lesson = build_pattern_lesson("lavar", day_key=12, track=TRACK_IRREGULAR)
        self.assertIn("usage_lesson", lesson)
        self.assertIn("pattern_formulas", lesson)
        self.assertIn("native_examples", lesson)
        self.assertIn("production_drills", lesson)
        self.assertIn("freestyle_drills", lesson)
        self.assertIn("mistake_repair", lesson)
        self.assertIn("pattern_repetition", lesson)
        self.assertEqual(len(lesson["native_examples"]), 10)
        self.assertGreaterEqual(len(lesson["production_drills"]), 1)
        self.assertEqual(len(lesson["pattern_repetition"]["variations"]), 10)

    def test_pattern_formulas_include_verb(self) -> None:
        lesson = build_pattern_lesson("volver", day_key=8, track=TRACK_IRREGULAR)
        formulas = lesson["pattern_formulas"]
        self.assertTrue(formulas)
        self.assertTrue(any("volver" in row["formula"].lower() for row in formulas))

    def test_pattern_repetition_contains_context_words(self) -> None:
        lesson = build_pattern_lesson("pedir", day_key=6, track=TRACK_PARETO)
        repetition = lesson["pattern_repetition"]
        self.assertTrue(repetition["primary_pattern"])
        self.assertTrue(all(row["context_word"] for row in repetition["variations"]))


class TestEmailBody(unittest.TestCase):
    def test_email_body_renders_pattern_sections(self) -> None:
        ex = select_daily_exercise(seed=3, track=TRACK_IRREGULAR)
        verb = ex["verb"]
        day_key = _day_key(3)
        native = select_native_lesson(day_key, TRACK_IRREGULAR)
        pattern_lesson = build_pattern_lesson(verb, day_key=day_key, track=TRACK_IRREGULAR)
        plain, html, att_plain, att_name = build_daily_exercise_body(
            verb,
            ex["assignments"],
            category=ex.get("category", ""),
            pattern_lesson=pattern_lesson,
            native_lesson=native,
        )
        vu = verb.upper()
        self.assertIn(vu, plain)
        self.assertIn("Part 1", plain)
        self.assertIn("Conjugation", plain)
        self.assertIn("Part 2 — Verb usage lesson", plain)
        self.assertIn("Part 3 — Pattern formulas", plain)
        self.assertIn("Part 4 — Native examples", plain)
        self.assertIn("Part 5 — Pattern production exercises", plain)
        self.assertIn("Part 6 — Freestyle drills", plain)
        self.assertIn("Part 7 — Common mistake repair", plain)
        self.assertIn("Part 8 — Pattern repetition drill", plain)
        self.assertNotIn("Part 2 — Sentence practice", plain)
        self.assertNotIn("Translate each English prompt", plain)
        self.assertIn(vu, html)
        self.assertIn("<ol>", html)
        self.assertIn(f"Write {len(ex['assignments'])} lines", plain)
        self.assertTrue(len(plain) > 300)
        self.assertTrue(len(html) > 300)
        self.assertIsNone(att_plain)
        self.assertIsNone(att_name)


class TestMainImport(unittest.TestCase):
    def test_main_module_imports(self) -> None:
        import main  # noqa: F401 — exercise import graph

        self.assertTrue(hasattr(main, "cmd_send_daily"))


if __name__ == "__main__":
    unittest.main()
