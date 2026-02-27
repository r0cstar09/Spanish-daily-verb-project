# Daily Spanish Verb Trainer

A small tool that emails you **one** daily Spanish verb exercise: one verb, all five pronouns in all five tenses (Present, Future, Preterite, Imperfect, Conditional) — 25 conjugations total. You conjugate and submit to ChatGPT for grading.

**Design:** One verb per day from the list, every pronoun × every tense. No LLM in the app — you grade yourself in ChatGPT.

---

## Quick start

```bash
cd spanish-daily-verb-project
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# Create .env with EMAIL_USER, EMAIL_PASSWORD, TARGET_EMAIL (see below)

python main.py send-daily
```

---

## Setup

### 1. Python

Python 3.10+ recommended.

### 2. Gmail (or other email)

Use Gmail with an [App Password](https://support.google.com/accounts/answer/185833). In `.env`:

- `EMAIL_USER` = your Gmail address  
- `EMAIL_PASSWORD` = the 16-character app password (no spaces)  
- `TARGET_EMAIL` = where to send the daily exercise (usually the same)

For non-Gmail, set `SMTP_HOST` and `SMTP_PORT` as needed.

### 3. Environment variables

| Variable          | Description                    |
|-------------------|--------------------------------|
| `EMAIL_USER`      | SMTP login (e.g. Gmail)        |
| `EMAIL_PASSWORD`  | App password (not normal pwd) |
| `TARGET_EMAIL`    | Recipient of the daily exercise |
| `SMTP_HOST`       | Default `smtp.gmail.com`       |
| `SMTP_PORT`       | Default `587`                  |

No OpenAI or Azure keys needed — evaluation is up to you (e.g. in ChatGPT).

---

## Usage

```bash
python main.py send-daily
```

- Picks one verb from the list.
- Sends one email to `TARGET_EMAIL` with the verb and 25 lines (every pronoun in every tense: Present, Future, Preterite, Imperfect, Conditional). You conjugate all 25 and submit to ChatGPT for grading.

**Reproducible run:**  
`python main.py send-daily --seed 42` uses a fixed random seed.

---

## GitHub Actions

One workflow sends the daily exercise on a schedule.

1. **Add repository secrets** (Settings → Secrets and variables → Actions):
   - `EMAIL_USER` — your Gmail address  
   - `EMAIL_PASSWORD` — Gmail App Password  
   - `TARGET_EMAIL` — where to send the exercise  

2. **Push** the repo. The workflow runs once per day at **10:00 UTC (5:00 AM Eastern)**. Change the `cron` in `.github/workflows/send-daily.yml` to change the time.

3. **Run manually:** Actions → "Send daily exercise" → Run workflow.

**Note:** Gmail may flag logins from GitHub. Use an App Password and allow the sign-in if prompted.

---

## Cron (local)

To run send-daily on your own machine:

```cron
0 8 * * * cd /path/to/spanish-daily-verb-project && .venv/bin/python main.py send-daily
```

---

## Project layout

| File / folder     | Purpose |
|--------------------|--------|
| `main.py`          | CLI: `send-daily` only |
| `verb_selector.py` | Picks one verb; returns all 5 pronouns × 5 tenses (25 conjugations) |
| `translations.py`  | Generates English translations for each pronoun+tense |
| `verb_translations.json` | Spanish→English verb forms (base, past, irregulars) |
| `verbs.json`       | 60 common Spanish verbs |
| `email_sender.py`  | Sends the daily exercise email (SMTP) |
| `.env`             | Secrets (gitignored) |
| `docs/example_emails.md` | Example daily exercise email |

---

## Example daily email

**Subject:** `Spanish Verb – LLEVAR (all tenses)`

**Body:** Verb + 25 lines, each with pronoun, tense, and English translation (e.g. `yo (Present) — I need`).  
Then: *Submit your 25 conjugations to ChatGPT for grading.*

---

## Dependencies

- **python-dotenv** — loads `.env`.  
- Standard library: `smtplib`, `email`, `json`, `random`, `pathlib`.

---

## License

Use and modify as you like.
