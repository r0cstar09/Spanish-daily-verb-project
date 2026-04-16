"""Shared helpers for building polysemous sentence banks (120 lines, sense + optional lesson tags)."""

from __future__ import annotations

# Rotating grammar/native tags attached to some lines (not every line — avoid clutter).
LESSON_TAGS = (
    "reflexive",
    "clitic",
    "collocation",
    "subjunctive_cue",
    "ser_estar",
    "register",
    "por_para",
    "native_idiom",
)


def bank_from_rows(rows: list[tuple[str, str] | tuple[str, str, str | None]]) -> list[dict]:
    """
    rows: (en, sense) or (en, sense, lesson) — truncated/padded to exactly 120.
    """
    normalized: list[tuple[str, str, str | None]] = []
    for row in rows:
        if len(row) == 2:
            en, sense = row
            normalized.append((en, sense, None))
        else:
            en, sense, lesson = row
            normalized.append((en, sense, lesson))

    if len(normalized) < 120:
        # Cycle-extend with numbered variants so rotation still has distinct lines.
        k = 0
        while len(normalized) < 120:
            en, sense, lesson = normalized[k % len(normalized)]
            normalized.append((f"{en} (rephrase {k // len(normalized) + 1})", sense, lesson))
            k += 1

    out: list[dict] = []
    for i, (en, sense, lesson) in enumerate(normalized[:120]):
        d: dict = {"id": i + 1, "en": en, "sense": sense}
        if lesson:
            d["lesson"] = lesson
        out.append(d)
    return out


def add_lessons_every(
    lines: list[tuple[str, str]],
    every: int = 4,
) -> list[tuple[str, str, str | None]]:
    """Attach rotating lesson tags to every `every` lines."""
    out: list[tuple[str, str, str | None]] = []
    for i, (en, sense) in enumerate(lines):
        if i % every == 0:
            les = LESSON_TAGS[i // every % len(LESSON_TAGS)]
            out.append((en, sense, les))
        else:
            out.append((en, sense, None))
    return out


def flatten_blocks(
    blocks: list[tuple[str, list[str]]],
    lesson_every: int = 4,
) -> list[tuple[str, str] | tuple[str, str, str | None]]:
    """blocks: (sense_tag, [english lines...])."""
    lines: list[tuple[str, str]] = []
    for sense, ens in blocks:
        for en in ens:
            lines.append((en, sense))
    tagged = add_lessons_every(lines, every=lesson_every)
    return tagged


def build_multisense_from_specs(
    specs: list[tuple[str, int, list[str] | tuple[str, ...]]],
    lesson_every: int = 4,
) -> list[dict]:
    """
    specs: list of (sense_tag, count, templates) where templates is a list/tuple of
    format strings using {i} (0..count-1). len(templates) can be < count — cycles.
    Total counts must sum to 120.
    """
    lines: list[tuple[str, str]] = []
    for sense, count, tmpl_list in specs:
        tmpls = list(tmpl_list)
        for i in range(count):
            t = tmpls[i % len(tmpls)]
            lines.append((t.format(i=i), sense))
    assert len(lines) == 120, len(lines)
    return bank_from_rows(add_lessons_every(lines, every=lesson_every))
