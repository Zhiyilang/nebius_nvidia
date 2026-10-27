# Nebius Personal AI — Nemotron-powered private assistant

A **Personal AI** entry for the **Nebius × NVIDIA Global AI Hackathon 2026**
(Personal AI track). It is a private, always-on assistant with **persistent
memory**, **reusable skills** (user-controlled tools), and reasoning powered by
**NVIDIA Nemotron** served on **Nebius Token Factory**.

- Persistent memory across sessions (local append-only store)
- Reusable skills: `remember`, `recall`, `remind`
- Calls Nemotron through the Nebius OpenAI-compatible endpoint
- **Zero third-party dependencies** (Python standard library only)

## Why this fits the Personal AI track
The brief asks for "an always-on, private assistant that works for you while
keeping your data under your control. Give it persistent memory, reusable
skills, access to the tools and information you choose." This project delivers
exactly that: memory survives restarts, the three skills are reusable, and no
data leaves the user's machine except the chat text sent to the user's own
Nebius endpoint.

## Setup (you do this — "register / get key")
1. Join the hackathon on Devpost: <https://nebiusglobalaihackathon.devpost.com/>
2. Create a **Nebius Token Factory** account and finish billing onboarding
   (needs a bank card; new users get trial credit).
3. Grab the **$25 hackathon credit** with code `NEBIUS-DEVPOST-GLOBAL26`.
4. Create an API key and export it:

```bash
export NEBIUS_API_KEY="sk-..."          # your key, never hard-coded
export NEBIUS_MODEL="ai-ngu/Nemotron-3-Nano"   # swap to ...-Ultra for heavy reasoning
```

> Verify the exact model id in the Nebius model catalog; the default above is a
> sensible starting point.

## Run
```bash
python app.py          # CLI chat loop
# or as a demo web service:
PORT=8000 python serve.py
```

`serve.py` exposes `GET /` (health) and `POST /chat` (`{"message": "..."}` →
`{"reply": "..."}`), so you can host the demo on any PaaS (Hugging Face Space,
Render, a VM) to satisfy the "working demo URL" requirement.

## Verify locally (no key needed)
```bash
python eval.py         # 9 checks, exit 0
```
The live Nemotron call is intentionally not asserted by `eval.py` — it needs
your key. After exporting `NEBIUS_API_KEY`, run `python app.py` and chat to
confirm end-to-end behaviour.

## Submission checklist (Devpost)
- [ ] Public GitHub repo with MIT license + this README
- [ ] Working demo URL (host `serve.py`) or screen-share
- [ ] Public YouTube video ≤ 3 min showing it working on Nemotron / Token Factory
- [ ] Project description (why / how)
- [ ] Pick **Personal AI** track
- [ ] Feedback on Nebius Token Factory + NVIDIA models

See `SUBMISSION.md` for the copy-ready write-up.
