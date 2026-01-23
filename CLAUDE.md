# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Gradio-based psychoanalytic personality assessment web application. Users answer 18 questions across 8 personality types (Narcissistic, Obsessive, Depressive, Paranoid, Schizoid, Hysterical, Borderline, Masochistic), then receive LLM-powered analysis via Claude API.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application (launches at http://localhost:7860)
python app.py
```

**Note:** Requires `ANTHROPIC_API_KEY` in `.env` file for LLM analysis. Without it, the app falls back to pattern-matching analysis.

## Architecture

This is a **single-file application** (`app.py`, ~1100 lines) with these components:

1. **Question Bank** (lines 13-284): 18 questions, each with 8 personality-type response options
2. **API Integration** (lines 286-358): `call_claude_api()` and `analyze_with_llm()` for Claude API calls
3. **Fallback Analysis** (lines 360-407): `fallback_analysis()` - pattern-matching when API unavailable
4. **Export Functions** (lines 434-641): Word (.docx) and Markdown (.md) export via `python-docx`
5. **File I/O** (lines 434-743): JSON upload/save, filename generation, path validation
6. **Gradio UI** (lines 820-1094): 3-tab interface (Assessment, Upload, Save)

**Processing Flow:**
```
User answers 18 questions
    → process_assessment() collects responses as JSON
    → analyze_with_llm() or fallback_analysis()
    → Display analysis + JSON
    → Optional export to Word/Markdown
```

## Key Files

| File | Purpose |
|------|---------|
| `app.py` | Main application (all code in single file) |
| `requirements.txt` | Dependencies: gradio, python-docx, python-dotenv |
| `.env` | API keys (ANTHROPIC_API_KEY required for LLM analysis) |
| `README1.md` | Full technical documentation |

## Deployment

- **Local:** `python app.py`
- **Hugging Face Spaces:** Configured via `README.md` metadata (Gradio SDK 6.2.0)