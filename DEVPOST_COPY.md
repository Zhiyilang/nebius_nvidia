# Nebius × NVIDIA — Devpost 提交复制包（copy-paste）

> 用法：登录 Devpost → 加入 `nebiusglobalaihackathon` → Submit Project。
> 把下面三段分别粘进对应字段，仅 3 个 `[ ]` 占位需你填（demo URL / 视频 / 仓）。
> 前提：已 `git push` 本仓到 GitHub 公开仓（见 `GITHUB_PUSH_COMMANDS.md` 的 Nebius 段）。

---

## 1) Project Title
**Nebius Personal AI** — a private, memory-bearing assistant on NVIDIA Nemotron + Nebius Token Factory

## 2) Summary（一句话，≤140 字符）
A private Personal AI with persistent local memory and reusable tools, powered by NVIDIA Nemotron on Nebius Token Factory.

## 3) Description（完整描述，直接粘）
**What I built**
Nebius Personal AI is a Personal-AI assistant that keeps **persistent memory** across sessions and owns **reusable skills** (user-controlled tools): `remember`, `recall`, and `remind`. All reasoning runs on **NVIDIA Nemotron** served through **Nebius Token Factory**, so the heavy lifting stays on open infrastructure while the user's data never leaves their machine.

**Why I built it**
The brief defines Personal AI as "an always-on, private assistant that works for you while keeping your data under your control … persistent memory, reusable skills, access to the tools and information you choose." Most assistants forget everything between sessions and leak context to third parties. This project closes both gaps: memory is an append-only local store, and the only thing sent to the cloud is the chat text to the user's own Nebius endpoint.

**How it works**
1. User message → assistant keeps a rolling conversation history.
2. Nemotron (via Token Factory) decides whether to call a tool.
3. Tools write/read the local memory store (`remember` / `recall` / `remind`).
4. Tool results are fed back to the model for a grounded final answer.
5. `serve.py` wraps the assistant in a tiny HTTP service for the demo URL.

Memory is file-backed and survives restarts — proven by the eval suite (`python eval.py`, 9/9 green): store a fact, restart, recall it, set a reminder, and the reminder fires on schedule.

**Track:** Personal AI

**NVIDIA / Nebius usage**
- Model: NVIDIA **Nemotron** (`ai-ngu/Nemotron-3-Nano`, swap to `-Ultra` for heavy reasoning) served on **Nebius Token Factory**.
- Every LLM call goes through Nebius's OpenAI-compatible endpoint; no other provider is used.
- Feedback: Token Factory onboarding was smooth; the OpenAI-compatible surface meant zero SDK lock-in, and trial credit covered all dev calls.

**Demo**
- Live demo URL: [ 你的 serve.py 公网地址，或 HF Space 链接 ]
- YouTube video (≤3 min, Public): [ 你的演示视频链接 ]
- Repo: [ 你的公开 GitHub 仓链接 ]

**License:** MIT

## 4) Category / Track
Personal AI

## 5) Feedback on Nebius Token Factory / NVIDIA
Token Factory onboarding was smooth and the OpenAI-compatible API meant I could swap models (Nano ↔ Ultra) with a one-line change. Trial credit covered all development calls. Using Nemotron through open infrastructure kept the whole stack reproducible and credit-efficient.

---

### 你只需填的 3 个占位
- `[ 你的 serve.py 公网地址，或 HF Space 链接 ]`
- `[ 你的演示视频链接 ]`
- `[ 你的公开 GitHub 仓链接 ]`

其余文字全部可直接粘贴，无需改写。
