# Daily Spanish Verb Trainer

A small tool that emails you **one** daily Spanish verb exercise: one verb, mixed tenses across five pronouns. You practice your 5 sentences and get evaluated in ChatGPT (or however you like).

**Design:** One verb per day, one random tense per pronoun, low cognitive load. No LLM in the app — you evaluate yourself in ChatGPT.

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

- Picks one verb from the list and a random tense for each pronoun (Present, Preterite, Imperfect, Future).
- Sends one email to `TARGET_EMAIL` with the verb and 5 lines (pronoun + tense). You write 5 sentences and evaluate them yourself (e.g. in ChatGPT).

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
| `verb_selector.py` | Picks one verb + random tense per pronoun |
| `verbs.json`       | 60 common Spanish verbs |
| `email_sender.py`  | Sends the daily exercise email (SMTP) |
| `.env`             | Secrets (gitignored) |
| `docs/example_emails.md` | Example daily exercise email |

---

## Example daily email

**Subject:** `Spanish Verb – LLEVAR (mixed tenses)`

**Body:** Verb + 5 lines like: `1. yo (Future)`, `2. tú (Imperfect)`, …  
Then: *Practice your 5 sentences and get evaluated in ChatGPT or however you like.*

---

## Dependencies

- **python-dotenv** — loads `.env`.  
- Standard library: `smtplib`, `email`, `json`, `random`, `pathlib`.

---

## License

Use and modify as you like.
