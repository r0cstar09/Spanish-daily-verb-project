"""
Rotating "native-style" micro-lessons for each email (reflexives, clitics, discourse, etc.).

Picked deterministically from calendar day + track so you can preview with --seed.
"""

from __future__ import annotations

# Short tips — not full grammar lessons; meant to prime what to watch for in production.
NATIVE_LESSONS: list[str] = [
    "Reflexive verbs (me/te/se/nos/os/se): Spanish often uses a reflexive where English uses an intransitive or a different verb (e.g. *acordarse*, *quejarse*). Match the subject to the reflexive pronoun.",
    "Pronominal verbs: some verbs exist only or mainly with *se* (*arrepentirse*, *atreverse*). If the prompt implies 'oneself', consider *-se*.",
    "Clitic placement: with infinitives and gerunds, object clitics can attach (*decirlo*) or precede the finite verb (*lo voy a decir*) — both are natural; stay consistent in a given sentence.",
    "Double object (*le/lo*): people vs things (*le dije la verdad* / *se lo dije*). When both appear, *se* often replaces *le* (*se lo dije*).",
    "Ser vs estar: permanent/identity/category (*ser*) vs state/location/result (*estar*). Some adjectives change meaning (*listo* clever vs ready).",
    "Gustar-like verbs (*gustar, importar, molestar*): the thing 'does' the pleasing; the person is an indirect object (*me gusta / me gustan*).",
    "Impersonal *haber*: *hay* for existence; avoid plural agreement with the noun (*hay problemas*).",
    "*Hacer* time/weather: *hace calor*, *hace tres años* — different from English 'it is / it has been'.",
    "Subjunctive triggers: doubt, emotion, desire, non-existence, *para que*, *sin que*, *cuando* (future), *aunque* (concessive) — cue the mood from the English nuance.",
    "Por vs para: cause/medium/deadline path (*por*) vs goal/recipient/deadline point (*para*).",
    "Preterite vs imperfect: completed event vs background, habit, or ongoing in the past.",
    "Periphrastic future (*ir a* + infinitive) vs simple future: both natural; *ir a* often sounds more immediate.",
    "Diminutives (*-ito/-ita*): soften tone or indicate small size; common in spoken Spanish.",
    "Discourse markers: *pues*, *bueno*, *vamos a ver*, *o sea*, *es decir* — sprinkle sparingly for natural dialogue, not every sentence.",
    "Register: *tú* vs *usted* vs *vosotros* (Spain) — match the social situation you imagine for the prompt.",
    "Word order: new information often comes late; object pronouns are never postponed to the end like English.",
    "Negation: *no* before the conjugated verb; *nunca*, *nadie*, *nada* can double-negate naturally (*no veo a nadie*).",
    "Comparatives: *más/menos ... que*; *tan ... como*; *tanto ... como* for equality.",
    "Relative clauses: *que*, *quien*, *el cual*; *lo que* for 'what'. Avoid English-style *which* calques.",
    "Passive/se passive: *se vende*, *se habla español* — natural for general statements without naming an agent.",
    "Conditional for politeness: *¿Podría ...?*, *me gustaría ...* — softer than bare present.",
    "Commands: affirmative vs negative placement of clitics (*dímelo* vs *no me lo digas*).",
    "Gerund (*-ando/-iendo*): progressive aspect with *estar*; avoid overusing English '-ing' where Spanish prefers finite verb or infinitive.",
    "Infinitive after prepositions: *antes de*, *después de*, *sin*, *al* + infinitive — no *de* before infinitive in Spanish where English uses 'to'.",
    "Agreement: past participles with *haber* are invariable; with *estar* or pronouns they may agree (*está cansada*, *la he visto*).",
    "Verbal periphrasis: *tener que*, *deber*, *poder*, *soler*, *empezar a*, *volver a* — nuance of obligation, habit, repetition.",
    "Articles: Spanish uses definite articles more often (*me gusta el café*). Omission rules differ from English.",
    "Questions: subject can follow verb (*¿Viene Juan?*); rising intonation alone is not enough in writing — use ¿?",
    "Cleft-like focus: *es ... que*, *lo que* — natural emphasis without sounding translated.",
    "Connectors: *además*, *sin embargo*, *por eso*, *aun así* — paragraph flow in writing.",
    "Avoid Anglicisms: *eventualmente* ≠ eventually (*finalmente*); *actualmente* = currently (*actual* = current).",
    "Orthography: accents mark stress and distinguish *sí*/*si*, *más*/*mas*, *tú*/*tu*, *él*/*el*.",
]

LESSON_TITLE = "Native-style tip (rotates daily)"


def lesson_index(day_key: int, track: str) -> int:
    h = sum(ord(c) for c in track)
    return (day_key * 17 + h * 13) % len(NATIVE_LESSONS)


def select_native_lesson(day_key: int, track: str) -> str:
    return NATIVE_LESSONS[lesson_index(day_key, track)]
