# Daily Spanish Verb Trainer

This project emails you **two** daily verb lessons (separate schedules):

1. **Pareto track** (`pareto`) — high-frequency regular verbs
2. **Irregular / stem track** (`irregular`) — priority irregulars, then stem-changing verbs

The system is now a **pattern acquisition engine**, not a translation trainer.

## Daily lesson flow

Each email follows this sequence:

1. Conjugation drill (existing 5 pronouns × 10 tenses)
2. Verb usage lesson
3. Pattern formulas
4. Native examples (with semantic English meaning)
5. Pattern production exercises
6. Freestyle drills
7. Common mistake repair
8. Pattern repetition drill

## Data sources used by the lesson generator

- `verb_usage_hints.json` for verb-specific usage patterns, prepositions, reflexive contrasts, and traps
- `mas frecuente palabras en espanol.txt` to bias high-frequency vocabulary in examples and drills
- `verb_translations.json` / `pareto_glosses.json` for conjugation-side English cues only

## Quick start

```bash
cd spanish-daily-verb-project
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Create .env with EMAIL_USER, EMAIL_PASSWORD, TARGET_EMAIL
python main.py send-daily --track pareto
python main.py send-daily --track irregular
```

## Setup

### Python

Python 3.10+ recommended.

### Gmail (or other email)

Use Gmail with an [App Password](https://support.google.com/accounts/answer/185833). In `.env`:

- `EMAIL_USER` — your Gmail address
- `EMAIL_PASSWORD` — the 16-character app password (no spaces)
- `TARGET_EMAIL` — where to send the lesson

For non-Gmail, set `SMTP_HOST` and `SMTP_PORT`.

### Environment variables

| Variable | Description |
|---|---|
| `EMAIL_USER` | SMTP login |
| `EMAIL_PASSWORD` | App password |
| `TARGET_EMAIL` | Recipient of the lesson |
| `SMTP_HOST` | Default `smtp.gmail.com` |
| `SMTP_PORT` | Default `587` |

## Usage

```bash
python main.py send-daily --track pareto
python main.py send-daily --track irregular
```

- `--track pareto`: one verb every two days from `pareto_regular`
- `--track irregular`: curriculum progression from irregular to stem-changing
- `--seed`: deterministic test run

## GitHub Actions

| Workflow | Cron (UTC) | Command |
|---|---|---|
| `send-daily-pareto.yml` | `10:00` | `python main.py send-daily --track pareto` |
| `send-daily-irregular.yml` | `18:00` | `python main.py send-daily --track irregular` |

Add repository secrets: `EMAIL_USER`, `EMAIL_PASSWORD`, `TARGET_EMAIL`.

## Project layout

| File / folder | Purpose |
|---|---|
| `main.py` | CLI entrypoint and send pipeline |
| `verb_selector.py` | Track scheduling and conjugation assignment matrix |
| `pattern_lesson.py` | Pattern-based lesson generator (usage, formulas, examples, drills) |
| `verb_usage_hints.json` | Verb-specific pattern data used by generator |
| `mas frecuente palabras en espanol.txt` | Frequent-vocabulary bias source |
| `email_sender.py` | Email rendering and SMTP send |
| `native_lessons.py` | Rotating daily native-style micro-tip |
| `verbs_by_category.json` | Verb lists by track/category |
| `.github/workflows/` | Scheduled daily sends |

## License

Use and modify as you like.
