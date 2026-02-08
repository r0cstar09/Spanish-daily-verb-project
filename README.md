# Daily Spanish Verb Trainer

A Python tool that emails you **one** daily Spanish verb exercise (one verb, mixed tenses across five pronouns), reads your reply from your inbox, evaluates your sentences with an LLM, and emails you corrections plus conjugation tables.

**Design:** Production-first learning — you write sentences *before* seeing conjugations. One verb per day, one random tense per pronoun, low cognitive load.

---

## Quick start

```bash
# Clone or cd into project
cd spanish-daily-verb-project

# Create venv and install
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Configure (copy and edit)
cp .env.example .env
# Edit .env with your email and OpenAI API key

# Send today's exercise
python main.py send-daily

# After you reply to that email, run (e.g. via cron or manually):
python main.py check-replies
```

---

## Setup (detailed)

### 1. Python

- Python 3.10+ recommended.

### 2. Gmail (or other email)

- **Sending (SMTP):** Use Gmail with an [App Password](https://support.google.com/accounts/answer/185833). Set in `.env`:
  - `EMAIL_USER` = your Gmail address  
  - `EMAIL_PASSWORD` = the 16-character app password  
  - `TARGET_EMAIL` = where to send the exercise (usually the same)

- **Reading replies (IMAP):** Same account; enable IMAP in Gmail settings. The script uses IMAP to find replies to the daily exercise and extract your five sentences.

- For non-Gmail, set `SMTP_HOST`, `SMTP_PORT`, `IMAP_HOST`, `IMAP_PORT` in `.env` as needed.

### 3. OpenAI (LLM evaluation)

- Create an API key at [OpenAI](https://platform.openai.com/api-keys).
- In `.env`: `OPENAI_API_KEY=sk-...`
- Optional: `LLM_MODEL=gpt-4o-mini` (default) or `gpt-4o` for stronger corrections.

### 4. Environment variables

Copy `.env.example` to `.env` and fill in:

| Variable          | Description                    |
|-------------------|--------------------------------|
| `EMAIL_USER`      | SMTP/IMAP login (e.g. Gmail)   |
| `EMAIL_PASSWORD`  | App password (not normal pwd)  |
| `TARGET_EMAIL`    | Recipient of exercise & feedback |
| `OPENAI_API_KEY`  | OpenAI API key                 |
| `SMTP_HOST`       | Default `smtp.gmail.com`       |
| `SMTP_PORT`       | Default `587`                  |
| `IMAP_HOST`       | Default `imap.gmail.com`       |
| `IMAP_PORT`       | Default `993`                  |
| `LLM_MODEL`       | Default `gpt-4o-mini`          |

---

## Usage

### Send daily exercise

```bash
python main.py send-daily
```

- Picks one verb and a random tense for each pronoun (Present, Preterite, Imperfect, Future).
- Saves that as “today’s exercise” in `state.json` (or in CI, `.github/spanish-verb-state.json`).
- Sends one email to `TARGET_EMAIL` with the verb and instructions (5 lines: pronoun + tense each).

**Testing with a fixed verb:**  
`python main.py send-daily --seed 42` keeps the random choice reproducible.

### Check replies and send feedback

```bash
python main.py check-replies
```

- Looks for a **pending** exercise (one that hasn’t had a reply processed yet).
- Fetches recent inbox messages that are replies to the daily exercise (not to the feedback email).
- Takes the **latest** such reply, extracts up to 5 Spanish sentences (ignoring quoted text and signatures).
- Sends your sentences + verb + per-line tense to the LLM for correction and conjugation tables.
- Emails you the feedback (corrected sentences, brief explanations, full conjugation table, short encouragement).
- Marks the reply as processed so the same reply isn’t handled again.

If there’s no pending exercise or no reply, the script exits without sending anything.

---

## GitHub Actions (recommended)

The repo includes workflows so everything runs in the cloud: daily exercise email on a schedule, and reply checks every 10 minutes.

### What you need to do

1. **Add repository secrets**  
   In your GitHub repo: **Settings → Secrets and variables → Actions**. Create these secrets (same values as in `.env`):

   | Secret name       | Value / notes |
   |-------------------|----------------|
   | `EMAIL_USER`      | Your Gmail address |
   | `EMAIL_PASSWORD`  | Gmail App Password (16 chars, no spaces) |
   | `TARGET_EMAIL`    | Where to send the exercise and feedback |
   | `OPENAI_API_KEY`  | Your OpenAI API key |

2. **Push the repo**  
   Push the branch that contains `.github/workflows/`. Actions will run on the schedule:
   - **Send daily exercise:** once per day at 10:00 UTC (5:00 AM Eastern). To change the time, edit the `cron` in `.github/workflows/send-daily.yml`.
   - **Check replies:** every 10 minutes. When you reply to the exercise email, the next run (within ~10 min) will pick it up and send you feedback.

3. **Optional: run manually**  
   In the repo go to **Actions**, choose "Send daily exercise" or "Check replies", and click **Run workflow**.

State is stored in `.github/spanish-verb-state.json` and committed by the workflows so the two jobs stay in sync. No other setup is required.

**Note:** Gmail may occasionally flag logins from GitHub’s servers. If sending or checking mail fails, check your Google account for a security alert and allow the sign-in, or use an App Password and ensure 2FA is on.

---

## Automation (cron, local)

If you prefer to run on your own machine instead of GitHub Actions:

- **Morning:** send the exercise once per day.

  ```cron
  0 8 * * * cd /path/to/spanish-daily-verb-project && .venv/bin/python main.py send-daily
  ```

- **Later:** run reply check every 15–30 minutes.

  ```cron
  */30 * * * * cd /path/to/spanish-daily-verb-project && .venv/bin/python main.py check-replies
  ```

---

## Project layout

| File / folder       | Purpose |
|---------------------|--------|
| `main.py`           | CLI: `send-daily`, `check-replies` |
| `verb_selector.py`  | Loads verbs, picks one verb + random tense per pronoun |
| `verbs.json`        | 60 common Spanish verbs (incl. irregulars) |
| `email_sender.py`   | Sends exercise and feedback emails (SMTP) |
| `email_reader.py`  | Fetches and parses replies (IMAP) |
| `llm_evaluator.py` | Builds prompt, calls OpenAI, parses JSON result |
| `state.py`          | Persists “today’s exercise” and reply status |
| `state.json`        | Current exercise (local; gitignored). In CI: `.github/spanish-verb-state.json` (committed) |
| `.env`              | Secrets (gitignored) |
| `docs/example_emails.md`   | Example exercise, reply, and feedback emails |
| `docs/sample_llm_prompt.md`| Sample LLM prompt and expected JSON |

---

## Example emails and LLM prompt

- **Example emails:** see [docs/example_emails.md](docs/example_emails.md).
- **Sample LLM prompt and response format:** see [docs/sample_llm_prompt.md](docs/sample_llm_prompt.md).

---

## Reply format

Reply to the daily exercise email with **five sentences** (one per pronoun), in order. You can number them or not; the script strips numbering and quoted/original message.

Example:

```
Yo llevé el libro.
Tú llevaste el bolso.
Ella llevó la maleta.
Nosotros llevamos las cajas.
Ellos llevaron el equipaje.
```

Do not include English in the reply body.

---

## Dependencies

- **openai** – LLM API for evaluation.
- **python-dotenv** – Loads `.env` into `os.environ` (optional; you can export variables instead).

Standard library only for: `smtplib`, `imaplib`, `email`, `json`, `random`, `pathlib`, `re`.

---

## License

Use and modify as you like.
