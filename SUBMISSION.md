# Devpost Submission Write-up — Nebius Personal AI

> Copy-paste ready. Fill the few `[ ]` brackets with your live links.

## Title
**Nebius Personal AI** — a private, memory-bearing assistant powered by NVIDIA
Nemotron on Nebius Token Factory.

## What I built
A Personal AI assistant that keeps **persistent memory** across sessions and owns
**reusable skills** (user-controlled tools): `remember`, `recall`, and `remind`.
Reasoning runs on **NVIDIA Nemotron** through **Nebius Token Factory**, so the
heavy lifting stays on open infrastructure while the user's data stays local.

## Why I built it
The brief defines Personal AI as "an always-on, private assistant that works for
you while keeping your data under your control … persistent memory, reusable
skills, access to the tools and information you choose." Most assistants forget
everything between sessions and leak context to third parties. This project
closes both gaps: memory is an append-only local store, and the only thing sent
to the cloud is the chat text to the user's own Nebius endpoint.

## How it works
1. User message → assistant keeps a rolling conversation history.
2. Nemotron (via Token Factory) decides whether to call a tool.
3. Tools write/read the local memory store (`remember` / `recall` / `remind`).
4. Tool results are fed back to the model for a final, grounded answer.
5. `serve.py` wraps the assistant in a tiny HTTP service for the demo URL.

## Track
**Personal AI**

## NVIDIA / Nebius usage
- Model: NVIDIA **Nemotron** (`ai-ngu/Nemotron-3-Nano`, swap to `-Ultra` for
  heavy reasoning) served on **Nebius Token Factory**.
- All LLM calls go through the Nebius OpenAI-compatible endpoint; no other
  provider is used.
- Feedback: Token Factory onboarding was smooth; the OpenAI-compatible surface
  meant zero SDK lock-in. Trial credit covered all dev calls.

## Demo
- Live demo URL: [ your hosted serve.py link ]
- YouTube video (≤3 min): [ your video link ]
- Repo: [ your public GitHub repo ]

## License
MIT
