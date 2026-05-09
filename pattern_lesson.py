"""
Pattern-based lesson generator for daily verb practice.

This replaces translation-style sentence banks with native-usage training:
- usage lesson
- formulas
- native examples
- production drills
- freestyle prompts
- mistake repair
- pattern repetition
"""

from __future__ import annotations

import random
import re
from functools import lru_cache
from pathlib import Path

from translations import get_english_base
from verb_usage import get_usage_hint

FREQUENT_WORDS_PATH = Path(__file__).resolve().parent / "mas frecuente palabras en espanol.txt"

PREPOSITIONS = ("a", "de", "con", "en", "por", "para", "sin", "hacia", "sobre")
DEFAULT_INFINITIVES = ["hablar", "estudiar", "comer", "vivir", "viajar", "descansar"]
DEFAULT_ADJECTIVES = ["listo", "cansado", "tranquilo", "ocupado", "feliz", "seguro"]
DEFAULT_PLACES = ["la oficina", "la casa", "el mercado", "la estación", "el centro", "el barrio"]
DEFAULT_PEOPLE = ["mi amiga", "mi hermano", "el cliente", "el profesor", "mi vecina", "el equipo"]
DEFAULT_OBJECTS = ["la ropa", "la mesa", "el proyecto", "la puerta", "el informe", "la comida"]
DEFAULT_BODY_PARTS = ["las manos", "la cara", "el pelo", "los ojos", "los brazos", "los dientes"]


@lru_cache(maxsize=1)
def _load_frequent_words() -> list[str]:
    """
    Load high-frequency Spanish vocabulary from the local text file.
    """
    if not FREQUENT_WORDS_PATH.is_file():
        return []
    words: list[str] = []
    with open(FREQUENT_WORDS_PATH, encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if "\t" not in line:
                continue
            right = line.split("\t", 1)[1].strip()
            token = right.split()[0].lower()
            token = re.sub(r"[^a-záéíóúñü]", "", token)
            if len(token) >= 3:
                words.append(token)
    # Preserve order but drop duplicates.
    deduped = list(dict.fromkeys(words))
    return deduped


def _seed_for(verb: str, day_key: int, track: str) -> int:
    text = f"{verb.strip().lower()}|{track.strip().lower()}|{day_key}"
    return sum((i + 1) * ord(ch) for i, ch in enumerate(text))


def _parse_formulas(verb: str, usage_hint: str) -> list[dict[str, str]]:
    hint = (usage_hint or "").strip()
    if not hint:
        return [{"formula": f"{verb} + objeto", "meaning": "use the verb with a direct object in natural context"}]

    normalized = (
        hint.replace(" - ", " — ")
        .replace("–", "—")
        .replace("  ", " ")
        .strip()
    )
    parts = [p.strip(" .") for p in normalized.split(";") if p.strip()]

    formulas: list[dict[str, str]] = []
    for part in parts:
        if "—" in part:
            left, right = part.split("—", 1)
            formula = left.strip(" .")
            meaning = right.strip(" .")
        else:
            formula = part.strip(" .")
            meaning = "native usage pattern"
        if formula:
            formulas.append({"formula": formula, "meaning": meaning})

    if not formulas:
        formulas.append({"formula": f"{verb} + objeto", "meaning": "use the verb with a direct object"})

    out: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in formulas:
        key = row["formula"].lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


def _extract_prepositions(formulas: list[dict[str, str]]) -> list[str]:
    found: list[str] = []
    for f in formulas:
        text = f["formula"].lower()
        for prep in PREPOSITIONS:
            if re.search(rf"\b{prep}\b", text) and prep not in found:
                found.append(prep)
    return found


def _usage_lesson(verb: str, formulas: list[dict[str, str]], usage_hint: str) -> dict[str, object]:
    english_base = get_english_base(verb)
    core = (
        f"Core meaning: '{english_base}' in Spanish, but prioritize native collocations over direct translation."
        if english_base
        else "Core meaning: this verb should be learned as a usage pattern, not as a one-word translation."
    )

    reflexive = [f for f in formulas if "se" in f["formula"].lower()]
    non_reflexive = [f for f in formulas if "se" not in f["formula"].lower()]
    preps = _extract_prepositions(formulas)
    secondary = [f["meaning"] for f in formulas[1:3] if f["meaning"]]
    chunks = [f["formula"] for f in formulas[:4]]

    traps: list[str] = []
    low_hint = usage_hint.lower()
    if "not mean" in low_hint or "does not mean" in low_hint:
        traps.append("Avoid false-friend translation; this verb may differ from its English look-alike.")
    if "personal 'a'" in low_hint:
        traps.append("Remember personal 'a' with people when this verb takes a person as object.")
    if "no preposition" in low_hint:
        traps.append("Do not add extra prepositions copied from English.")
    if not traps:
        traps.append("Do not build word-for-word from English; retrieve the formula first, then fill content.")

    concept = (
        "Spanish packages meaning through chunks (verb + complement), so focus on reusable structures and context."
    )

    return {
        "core_meaning": core,
        "secondary_meanings": secondary,
        "reflexive_usage": [f"{r['formula']} = {r['meaning']}" for r in reflexive] or ["No dominant reflexive pattern listed."],
        "non_reflexive_usage": [f"{r['formula']} = {r['meaning']}" for r in non_reflexive] or ["No dominant non-reflexive pattern listed."],
        "common_prepositions": preps or ["none highlighted"],
        "idiomatic_chunks": chunks,
        "semantic_patterns": [f"{f['formula']} => {f['meaning']}" for f in formulas[:5]],
        "english_speaker_traps": traps,
        "conceptualization": concept,
    }


def _pick_from(pool: list[str], default: list[str], rng: random.Random, n: int) -> list[str]:
    source = pool if pool else default
    if len(source) >= n:
        return rng.sample(source, n)
    return [source[i % len(source)] for i in range(n)]


def _phrase_from_formula(verb: str, formula: str, rng: random.Random, freq_words: list[str]) -> str:
    phrase = formula.strip()
    phrase = re.sub(r"\s+", " ", phrase)

    freq_nouns = _pick_from(freq_words, [], rng, 8)
    objects = list(dict.fromkeys(DEFAULT_OBJECTS + freq_nouns[:4]))
    places = list(dict.fromkeys(DEFAULT_PLACES + [w for w in freq_nouns if w in {"casa", "oficina", "mercado", "parque", "ciudad"}]))
    people = list(dict.fromkeys(DEFAULT_PEOPLE))

    replacements = [
        (r"\+\s*(obj|algo|object)\b", " " + rng.choice(objects)),
        (r"\+\s*(body part|parte del cuerpo)\b", " " + rng.choice(DEFAULT_BODY_PARTS)),
        (r"\+\s*(person|persona|alguien)\b", " " + rng.choice(people)),
        (r"\+\s*(adjective|adj)\b", " " + rng.choice(DEFAULT_ADJECTIVES)),
        (r"\+\s*(place|lugar)\b", " " + rng.choice(places)),
        (r"\+\s*(gerund|gerundio)\b", " " + rng.choice(["trabajando", "estudiando", "caminando"])),
        (r"\+\s*(inf|infinitive|infinitivo)\b", " " + rng.choice(DEFAULT_INFINITIVES)),
    ]

    for pattern, repl in replacements:
        phrase = re.sub(pattern, repl, phrase, flags=re.IGNORECASE)

    phrase = phrase.replace("A por B", "una cosa por otra")
    phrase = phrase.replace("(Spain)", "").replace("(LatAm)", "").strip()

    low = phrase.lower()
    if f"{verb}se" in low:
        phrase = re.sub(rf"\b{re.escape(verb)}se\b", f"{verb}me", phrase, flags=re.IGNORECASE)

    return re.sub(r"\s+", " ", phrase).strip(" .")


def _native_examples(verb: str, formulas: list[dict[str, str]], day_key: int, track: str) -> list[dict[str, str]]:
    rng = random.Random(_seed_for(verb, day_key, track))
    freq_words = _load_frequent_words()
    templates = [
        "Hoy necesito {phrase}.",
        "En mi rutina suelo {phrase}.",
        "Esta semana quiero {phrase}.",
        "Normalmente podemos {phrase} sin problema.",
        "En el trabajo me toca {phrase}.",
    ]
    semantic_templates = [
        "Used to express: {meaning}.",
        "Natural intention: {meaning} in everyday context.",
        "Communicative goal: {meaning}.",
    ]

    out: list[dict[str, str]] = []
    for i in range(10):
        row = formulas[i % len(formulas)]
        phrase = _phrase_from_formula(verb, row["formula"], rng, freq_words)
        es = templates[i % len(templates)].format(phrase=phrase)
        meaning = row["meaning"] or "native usage in context"
        en = semantic_templates[i % len(semantic_templates)].format(meaning=meaning)
        out.append({"id": i + 1, "es": es, "en_semantic": en})
    return out


def _production_drills(formulas: list[dict[str, str]]) -> list[dict[str, str]]:
    drills: list[dict[str, str]] = []
    for i, row in enumerate(formulas[:6], start=1):
        drills.append(
            {
                "id": i,
                "pattern": row["formula"],
                "meaning": row["meaning"] or "express this idea naturally",
                "blank": "____________________________",
            }
        )
    if not drills:
        drills.append(
            {
                "id": 1,
                "pattern": "verbo + complemento",
                "meaning": "express the intended meaning with a native chunk",
                "blank": "____________________________",
            }
        )
    return drills


def _freestyle(formulas: list[dict[str, str]], rng: random.Random) -> list[dict[str, str]]:
    picks = formulas[:2] if len(formulas) >= 2 else formulas
    if not picks:
        picks = [{"formula": "verbo + complemento", "meaning": "general native usage"}]
    words = _pick_from(_load_frequent_words(), ["casa", "trabajo", "familia", "tiempo", "comida"], rng, 6)
    prompts: list[dict[str, str]] = []
    for row in picks:
        prompts.append(
            {
                "pattern": row["formula"],
                "instruction": "Create 5 original sentences using common vocabulary.",
                "vocab_bias": ", ".join(words[:3]),
            }
        )
    return prompts


def _mistake_repair(verb: str, formulas: list[dict[str, str]], usage_hint: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in formulas[:3]:
        formula = row["formula"]
        low = formula.lower()
        if "se" in low:
            incorrect = formula.replace("se", "", 1).strip()
            correction = formula
            why = "This pattern is pronominal/reflexive; dropping 'se' changes or breaks the meaning."
        elif any(f" {p} " in f" {low} " for p in PREPOSITIONS):
            incorrect = re.sub(r"\b(de|a|con|en|por|para|sin)\b", "a", formula, count=1, flags=re.IGNORECASE)
            correction = formula
            why = "This verb pattern selects a specific preposition; changing it sounds non-native."
        else:
            incorrect = f"{formula} (word-for-word from English)"
            correction = formula
            why = "Spanish favors stored chunks, not direct transfer from English syntax."
        rows.append({"incorrect": incorrect, "correction": correction, "why": why})

    if "not" in usage_hint.lower():
        rows.append(
            {
                "incorrect": "Using the English look-alike meaning automatically.",
                "correction": "Follow the usage pattern and collocation given for this verb.",
                "why": "Several Spanish verbs are false friends and need pattern-based meaning, not dictionary matching.",
            }
        )
    return rows[:4]


def _repetition_drill(primary_formula: dict[str, str], rng: random.Random) -> dict[str, object]:
    subjects = [
        ("yo", "presente"),
        ("tú", "presente"),
        ("él/ella", "pretérito"),
        ("nosotros", "imperfecto"),
        ("ellos/ellas", "futuro"),
        ("yo", "condicional"),
        ("tú", "presente perfecto"),
        ("él/ella", "subjuntivo presente"),
        ("nosotros", "subjuntivo imperfecto"),
        ("ellos/ellas", "perífrasis con estar + gerundio"),
    ]
    vocab = _pick_from(_load_frequent_words(), ["casa", "trabajo", "familia", "tiempo", "mercado"], rng, 10)
    variations = []
    for i, (subject, tense) in enumerate(subjects, start=1):
        variations.append(
            {
                "id": i,
                "subject": subject,
                "tense": tense,
                "context_word": vocab[i - 1],
                "prompt": "Write one sentence variation with this pattern and context.",
            }
        )
    return {
        "primary_pattern": primary_formula["formula"],
        "primary_meaning": primary_formula["meaning"] or "main communicative use",
        "variations": variations,
    }


def build_pattern_lesson(verb: str, *, day_key: int, track: str) -> dict[str, object]:
    """
    Build the full pattern-based lesson object for one verb.
    """
    v = verb.strip().lower()
    usage_hint = get_usage_hint(v)
    formulas = _parse_formulas(v, usage_hint)
    rng = random.Random(_seed_for(v, day_key, track))

    return {
        "verb": v,
        "usage_lesson": _usage_lesson(v, formulas, usage_hint),
        "pattern_formulas": formulas,
        "native_examples": _native_examples(v, formulas, day_key, track),
        "production_drills": _production_drills(formulas),
        "freestyle_drills": _freestyle(formulas, rng),
        "mistake_repair": _mistake_repair(v, formulas, usage_hint),
        "pattern_repetition": _repetition_drill(formulas[0], rng),
    }
