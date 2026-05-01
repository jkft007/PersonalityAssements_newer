# CLAUDE.md

Guidance for Claude Code when working in this repository.

---

## Project Overview

A Gradio-based psychoanalytic personality assessment web application.

Users answer 18 questions across 8 personality types (Narcissistic, Obsessive, Depressive, Paranoid, Schizoid, Hysterical, Borderline, Masochistic), then receive a dual-format LLM analysis (full narrative report + structured summary) via the Claude API. Profiles are saved as JSON and include chat history, conversation memories, and additional context that enriches re-analysis. A voice-enabled chat interface allows spoken interaction with the AI using the user's personality profile as context.

---

## Architecture

Single-file application: **`app.py`** (~1 400 lines).

### Functional sections

| Section | Description |
|---|---|
| Question bank | 18 questions × 8 personality-type answer options |
| API layer | `call_claude_api()` — shared Claude API caller with system-prompt and multi-turn support |
| Analysis | `analyze_narrative()` prose report · `analyze_summary()` bullet-point summary · `run_full_analysis()` runs both |
| Fallback analysis | `fallback_analysis()` — pattern-matching when no API key is set |
| Profile management | `create_profile()` · `save_profile_as_json()` · `load_profile_file()` · `_profile_to_saveable()` |
| Chat | `chat_with_profile()` · `initialize_chat()` · `generate_chat_welcome()` · `reanalyze_from_chat()` |
| Memory | `extract_memories()` parses `[MEMORY: ...]` tags from LLM responses and stores them in the profile |
| Voice | `transcribe_speech()` (OpenAI Whisper or Google STT) · `speak_response()` (gTTS) |
| Export | `export_to_word()` · `export_to_markdown()` |
| Gradio UI | 4-tab interface — Assessment · Profile · Chat · Save Results |

### Processing flows

```
Assessment:
  User answers 18 questions + optional extra info
      → process_assessment()
      → run_full_analysis()  [2 API calls: narrative + summary]
      → Display with Full Report / Summary toggle
      → Profile state created in-session

Chat:
  User opens Chat tab
      → initialize_chat()  [generates personalised welcome if chat is empty]
      → chat_with_profile()  [system prompt = personality analysis + memories]
      → extract_memories()  [auto-saves insights from each exchange]
      → Optional: speak_response()  [gTTS → autoplay audio]

Voice input:
  User records audio
      → transcribe_speech()  [Whisper API or Google STT]
      → chat_with_profile()
      → speak_response()  [always speaks for voice input]

Profile:
  Save  → _profile_to_saveable() strips narrative → JSON download
  Load  → load_profile_file() restores assessment, summary, extra info,
           memories, chat history, and radio button selections
```

### Profile JSON schema

```jsonc
{
  "profile_version": "1.0",
  "profile_id": "<uuid>",
  "subject_name": "",
  "created_at": "<iso8601>",
  "updated_at": "<iso8601>",
  "last_chat_at": "<iso8601> | null",
  "assessment": {                    // raw question responses
    "timestamp": "<iso8601>",
    "total_questions": 18,
    "responses": [ { "question_id": 1, "category": "...", "selected_type": "...", "selected_answer": "..." } ]
  },
  "analysis": "<summary text>",      // canonical stored version = summary
  "analysis_summary": "<summary>",   // bullet-point report (stored)
  // analysis_narrative is NOT stored — regenerated each session
  "extra_info": "",                  // free-text context provided by user
  "memories": [                      // auto-saved chat observations
    { "timestamp": "<iso8601>", "content": "<observation>" }
  ],
  "chat_history": [                  // full conversation log
    { "role": "user|assistant", "content": "..." }
  ]
}
```

---

## API Keys

| Key | Required | Purpose |
|---|---|---|
| `ANTHROPIC_API_KEY` | **Yes** | All LLM analysis and chat |
| `OPENAI_API_KEY` | No | OpenAI Whisper STT (higher accuracy). Falls back to Google STT if absent or if `openai` package missing. |

Set in `.env` at project root:

```
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...          # optional
```

---

## Chatbot Personalities

Five adult styles + two age-targeted:

| Personality | Therapeutic mode | TTS accent |
|---|---|---|
| Psychoanalytic | Unconscious patterns, defences, object relations | US English |
| Supportive | Warm, validating, strength-focused | British English |
| Socratic | Responds mainly with open questions | US English (slow) |
| Direct Coach | Action-oriented, concise, practical | Australian English |
| Empathic Listener | Reflective listening, validates before exploring | British English |
| Child Friendly (8–12) | Simple language, analogies, one question at a time | US English (slow) |
| Teen (13–17) | Direct, genuine, non-patronising, plain language | US English |

---

## Build & Local Development

### Prerequisites

- Python 3.11 or 3.13 (tested on 3.13)
- pip

### Install

```bash
# Clone / enter the repo
cd PersonalityAssements_newer

# Install all dependencies
pip install -r requirements.txt
```

### requirements.txt (current)

```
gradio>=6.1.0
python-docx
python-dotenv
gTTS
SpeechRecognition
openai          # optional — for Whisper STT
```

Update `requirements.txt` to match the above if it is out of date, then re-run `pip install -r requirements.txt`.

### Run locally

```bash
python app.py
# → http://localhost:7860
```

### Environment variables

```bash
# Windows PowerShell (session only)
$env:ANTHROPIC_API_KEY = "sk-ant-..."

# Or persist in .env (recommended)
echo ANTHROPIC_API_KEY=sk-ant-... > .env
```

### Microphone access (Windows)

Voice input requires browser microphone permission AND Windows privacy permission:

1. **Windows Settings → Privacy & Security → Microphone**
   - "Let apps access your microphone" → **On**
   - Scroll down and enable your browser explicitly
2. In the browser address bar click the **lock icon → Microphone → Allow**
3. Reload the page

---

## Deployment

### Option 1 — Hugging Face Spaces (current target)

`README.md` already contains the HF Spaces header:

```yaml
---
title: Personality
sdk: gradio
sdk_version: 6.2.0
app_file: app.py
---
```

**Steps:**

1. Push the repo to a Hugging Face Space (via `git push` or the HF web UI).
2. In the Space **Settings → Repository secrets**, add:
   - `ANTHROPIC_API_KEY`
   - `OPENAI_API_KEY` (optional)
3. HF Spaces will install `requirements.txt` automatically and run `app.py`.

**HF Spaces limitations:**

- No persistent disk — profiles must be downloaded by the user and re-uploaded each session. The JSON profile system is designed for this.
- Voice input (microphone) requires the Space to run over HTTPS, which HF Spaces provides by default — this is not an issue.
- gTTS requires internet access from the Space container (available on free tier).
- The narrative report (`analysis_narrative`) is never saved to disk — it is regenerated per session, which suits the stateless HF environment.

### Option 2 — Docker (self-hosted)

Create `Dockerfile` at project root:

```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY .env .          # or inject via --env-file at runtime

EXPOSE 7860

CMD ["python", "app.py"]
```

Build and run:

```bash
docker build -t personality-assessment .

# Pass API keys at runtime (preferred over baking into image)
docker run -p 7860:7860 \
  -e ANTHROPIC_API_KEY=sk-ant-... \
  -e OPENAI_API_KEY=sk-... \
  personality-assessment
```

Access at `http://localhost:7860`.

For HTTPS (needed for microphone in production), put an nginx or Caddy reverse proxy in front.

### Option 3 — Cloud VM (AWS / GCP / Azure)

1. Provision a small VM (1 vCPU, 1 GB RAM is sufficient — no GPU required).
2. Install Python 3.11+, clone the repo, install requirements.
3. Set API keys as environment variables or in `.env`.
4. Run behind a process manager:

```bash
# Install PM2 (or use systemd)
npm install -g pm2
pm2 start "python app.py" --name personality-app
pm2 save
pm2 startup
```

5. Add a reverse proxy (nginx + Let's Encrypt) for HTTPS — **required** for microphone to work in browsers on a public domain.

Sample nginx config:

```nginx
server {
    listen 443 ssl;
    server_name your.domain.com;

    ssl_certificate     /etc/letsencrypt/live/your.domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your.domain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:7860;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

---

## Key Files

| File | Purpose |
|---|---|
| `app.py` | Entire application — questions, logic, UI |
| `requirements.txt` | Python dependencies |
| `.env` | API keys (not committed) |
| `README.md` | Hugging Face Spaces configuration header |
| `CLAUDE.md` | This file |

---

## Important Constraints

- **Single-file design** — keep all code in `app.py`. Do not split into modules unless the file meaningfully exceeds ~2 000 lines.
- **Narrative not stored** — `analysis_narrative` is always regenerated; only `analysis_summary` is written to the profile JSON.
- **Stateless sessions** — the app holds no server-side user state. All persistence is via the profile JSON that the user downloads and re-uploads.
- **No auth** — the app has no authentication layer. For multi-user or public deployments, put an auth proxy in front (e.g. nginx basic auth, Cloudflare Access).
- **Educational use only** — this is not a clinical diagnostic tool. All analysis outputs should carry the disclaimer shown in the UI footer.
