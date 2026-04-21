# Daily Spanish Verb Trainer

A small tool that emails you **two** daily Spanish verb exercises (on separate schedules):

1. **Pareto track** — high-frequency **regular** verbs (`pareto_regular` in [`verbs_by_category.json`](verbs_by_category.json)).
2. **Irregular / stem track** — starts with high-priority **irregular** verbs first, then moves to **stem-changing** verbs.

Each email includes:

- **Part 1 — Conjugation:** five pronouns × **ten** tenses (50 lines): Present, Future, Preterite, Imperfect, Conditional, Present Perfect, Pluperfect, Present Subjunctive, Imperfect Subjunctive, Estar + Gerund.
- **Part 2 — Sentence practice:** **10** English prompts per email, **rotated** from the full committed bank for that verb (so the next time the same verb is scheduled you see a different slice). Polysemous verbs like **quedar** and **hacer** use meaning-tagged prompts in [`polysemous_content.py`](polysemous_content.py). Optional `[sense]` labels appear in the email for those lines.

English glosses use [`verb_translations.json`](verb_translations.json) for listed verbs and [`pareto_glosses.json`](pareto_glosses.json) for Pareto verbs. **Sentence banks live in the repo** as JSON under [`sentence_banks/`](sentence_banks/). The mailer **only reads** committed JSON — no API calls at send time.

---

## Quick start

```bash
cd spanish-daily-verb-project
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Sentence banks are committed in sentence_banks/ (validate with scripts/build_sentence_banks.py if needed).
# Create .env with EMAIL_USER, EMAIL_PASSWORD, TARGET_EMAIL

python main.py send-daily --track pareto
python main.py send-daily --track irregular
```

---

## Sentence banks (committed JSON)

Each verb has a file `sentence_banks/<verb>.json` with **120** English lines in the full bank (`id`, `en`, and optionally `sense` for polysemous verbs). The mailer sends **10** lines per email; which 10 is chosen by [`sentence_rotation.py`](sentence_rotation.py) from **calendar day**, **verb**, and **track** (and `--seed` when testing), so repeats of the same verb use a **different window** over time.

Validate committed banks with:

```bash
python scripts/build_sentence_banks.py
```

The script checks that each verb listed in [`verbs_by_category.json`](verbs_by_category.json)
has a corresponding `sentence_banks/<verb>.json` with non-empty `sentences`.
Scheduled sends **fail** if a bank is missing or has an empty `sentences` array.

---

## Setup

### Python

Python 3.10+ recommended.

### Gmail (or other email)

Use Gmail with an [App Password](https://support.google.com/accounts/answer/185833). In `.env`:

- `EMAIL_USER` — your Gmail address  
- `EMAIL_PASSWORD` — the 16-character app password (no spaces)  
- `TARGET_EMAIL` — where to send the daily exercise (usually the same)

For non-Gmail, set `SMTP_HOST` and `SMTP_PORT` as needed.

### Environment variables

| Variable          | Description                    |
|-------------------|--------------------------------|
| `EMAIL_USER`      | SMTP login (e.g. Gmail)        |
| `EMAIL_PASSWORD`  | App password (not normal pwd) |
| `TARGET_EMAIL`    | Recipient of the daily exercise |
| `SMTP_HOST`       | Default `smtp.gmail.com`       |
| `SMTP_PORT`       | Default `587`                  |

---

## Usage

```bash
python main.py send-daily --track pareto
python main.py send-daily --track irregular
```

- **`--track pareto`** — picks from `pareto_regular` with one verb every two days (or `--seed`).
- **`--track irregular`** — follows a curriculum day index: high-priority irregulars first, then stem-changing verbs.

**Reproducible run:**  
`python main.py send-daily --track pareto --seed 52` fixes selection for testing (seed semantics differ per track).

---

## GitHub Actions

Two workflows send on separate schedules:

| Workflow | Cron (UTC) | Command |
|----------|------------|---------|
| [Send daily exercise (Pareto)](.github/workflows/send-daily-pareto.yml) | 10:00 | `python main.py send-daily --track pareto` |
| [Send daily exercise (Irregular / stem)](.github/workflows/send-daily-irregular.yml) | 18:00 | `python main.py send-daily --track irregular` |

1. Add repository secrets: `EMAIL_USER`, `EMAIL_PASSWORD`, `TARGET_EMAIL`.  
2. Ensure all `sentence_banks/*.json` files are filled and committed before enabling schedules.  
3. Run manually: Actions → choose the workflow → Run workflow.

---

## Cron (local)

```cron
0 10 * * * cd /path/to/spanish-daily-verb-project && .venv/bin/python main.py send-daily --track pareto
0 18 * * * cd /path/to/spanish-daily-verb-project && .venv/bin/python main.py send-daily --track irregular
```

---

## Project layout

| File / folder | Purpose |
|---------------|--------|
| `main.py` | CLI: `send-daily --track …` |
| `verb_selector.py` | Picks verb per track; builds 50 conjugation lines |
| `tenses.py` | Shared list of tense names |
| `verbs_by_category.json` | `pareto_regular`, `irregular`, `stem_changing` |
| `pareto_glosses.json` | English bases for Pareto verbs (string or object with `base`/`past`/`pp`) |
| `translations.py` | English hints per pronoun+tense |
| `verb_translations.json` | Full glosses for irregular/stem verbs |
| `sentence_bank.py` | Loads `sentence_banks/<verb>.json` |
| `sentence_rotation.py` | Picks 10 prompts per send from the full bank (date + verb + track) |
| `polysemous_content.py` | Curated multi-meaning banks for **quedar** and **hacer** |
| `sentence_banks/` | One JSON file per infinitive (120 lines; quedar/hacer include `sense`) |
| `scripts/build_sentence_banks.py` | Validates committed `sentence_banks/*.json` coverage and shape |
| `email_sender.py` | Builds and sends email (optional attachment for long banks) |
| `.env` | Secrets (gitignored) |

---

## Dependencies

- **python-dotenv** — loads `.env` for `main.py`.  
- Standard library: `smtplib`, `email`, `json`, `pathlib`, `argparse`.

---

## License

Use and modify as you like.
