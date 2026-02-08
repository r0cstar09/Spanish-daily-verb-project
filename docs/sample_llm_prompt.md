# Sample LLM evaluation prompt

The evaluator sends a prompt like the following to the LLM (e.g. OpenAI). The model must respond with **valid JSON only**.

---

## Example prompt (verb: llevar, tense: Preterite)

```
You are a strict but kind Spanish teacher. Evaluate the following student sentences.

Verb (infinitive): llevar
Tense: Preterite
Expected pronouns in this order:
1. yo
2. tú
3. él/ella
4. nosotros/nosotras
5. ellos/ellas

Student's sentences (one per pronoun, in order):
1. Yo llevé el libro.
2. Tú llevas el bolso.
3. Ella llevó la maleta.
4. Nosotros llevamos las cajas.
5. Ellos llevaron el equipaje.

Respond with a valid JSON object only, no markdown or extra text. Use this exact structure:

{
  "results": [
    {
      "pronoun": "yo",
      "original": "exact student sentence",
      "correct": true or false,
      "corrected": "corrected sentence if wrong, otherwise same as original",
      "explanation": "brief explanation in simple English if wrong; if correct write 'Correct.'"
    }
  ],
  "conjugation_table": "yo [form]\ntú [form]\nél/ella [form]\nnosotros/nosotras [form]\nellos/ellas [form]",
  "encouragement": "One short sentence of encouragement or a pattern reminder."
}

Rules:
- Evaluate strictly: conjugation must match the requested tense and pronoun.
- For each of the 5 pronouns, output one entry in "results" in the same order: yo, tú, él/ella, nosotros/nosotras, ellos/ellas.
- If the student gave fewer than 5 sentences, still output 5 entries; use "original": "(missing)" and "correct": false for missing ones, and suggest a correct example in "corrected".
- conjugation_table: one line per pronoun with the conjugated form only (e.g. "yo llevé").
- Keep explanations very brief (one line).
- Output only the JSON object.
```

---

## Example JSON response

```json
{
  "results": [
    {
      "pronoun": "yo",
      "original": "Yo llevé el libro.",
      "correct": true,
      "corrected": "Yo llevé el libro.",
      "explanation": "Correct."
    },
    {
      "pronoun": "tú",
      "original": "Tú llevas el bolso.",
      "correct": false,
      "corrected": "Tú llevaste el bolso.",
      "explanation": "Preterite requires llevaste; llevas is present tense."
    },
    {
      "pronoun": "él/ella",
      "original": "Ella llevó la maleta.",
      "correct": true,
      "corrected": "Ella llevó la maleta.",
      "explanation": "Correct."
    },
    {
      "pronoun": "nosotros/nosotras",
      "original": "Nosotros llevamos las cajas.",
      "correct": true,
      "corrected": "Nosotros llevamos las cajas.",
      "explanation": "Correct."
    },
    {
      "pronoun": "ellos/ellas",
      "original": "Ellos llevaron el equipaje.",
      "correct": true,
      "corrected": "Ellos llevaron el equipaje.",
      "explanation": "Correct."
    }
  ],
  "conjugation_table": "yo llevé\ntú llevaste\nél/ella llevó\nnosotros/nosotras llevamos\nellos/ellas llevaron",
  "encouragement": "Preterite -ar endings: -é, -aste, -ó, -amos, -aron. You had one mix-up with present vs preterite for tú."
}
```
