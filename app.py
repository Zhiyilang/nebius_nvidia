#!/usr/bin/env python3
"""Personal AI assistant powered by NVIDIA Nemotron via Nebius Token Factory.

Nebius x NVIDIA Global AI Hackathon 2026 -- Personal AI track.
- Persistent memory across sessions (local append-only store)
- Reusable skills / user-controlled tools (remember, recall, remind)
- Calls Nemotron through the Nebius OpenAI-compatible endpoint

Zero third-party dependencies: standard library only.
"""
import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta

BASE_URL = os.environ.get("NEBIUS_BASE_URL", "https://api.nebius.com/v1")
MODEL = os.environ.get("NEBIUS_MODEL", "ai-ngu/Nemotron-3-Nano")
API_KEY = os.environ.get("NEBIUS_API_KEY", "")
MEMORY_PATH = os.environ.get("MEMORY_PATH", "memory.jsonl")


def _post_chat(messages, tools=None):
    if not API_KEY:
        raise RuntimeError("NEBIUS_API_KEY not set")
    body = {"model": MODEL, "messages": messages, "temperature": 0.3}
    if tools:
        body["tools"] = tools
    req = urllib.request.Request(
        BASE_URL.rstrip("/") + "/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {API_KEY}",
                 "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


# ---- persistent memory ----
def memory_load():
    if not os.path.exists(MEMORY_PATH):
        return []
    out = []
    with open(MEMORY_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def memory_append(record):
    with open(MEMORY_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


# ---- tools (reusable skills, user-controlled) ----
TOOLS = [
    {"type": "function", "function": {
        "name": "remember",
        "description": "Store a durable fact, preference or note into long-term memory.",
        "parameters": {"type": "object",
                       "properties": {"content": {"type": "string"}},
                       "required": ["content"]}}},
    {"type": "function", "function": {
        "name": "recall",
        "description": "Search stored memory for items matching a query.",
        "parameters": {"type": "object",
                       "properties": {"query": {"type": "string"}},
                       "required": ["query"]}}},
    {"type": "function", "function": {
        "name": "remind",
        "description": "Set a reminder at a relative time (minutes from now).",
        "parameters": {"type": "object",
                       "properties": {"minutes": {"type": "integer"},
                                      "text": {"type": "string"}},
                       "required": ["minutes", "text"]}}},
]


def tool_remember(content):
    memory_append({"ts": datetime.now().isoformat(), "kind": "fact", "content": content})
    return f"Remembered: {content}"


def tool_recall(query):
    mem = memory_load()
    q = query.lower()
    hits = [m for m in mem if q in m.get("content", "").lower()]
    if not hits:
        return "No matching memory found."
    return "\n".join(f"- {h['content']}" for h in hits[-5:])


def tool_remind(minutes, text):
    due = datetime.now() + timedelta(minutes=minutes)
    memory_append({"ts": datetime.now().isoformat(), "kind": "reminder",
                   "due": due.isoformat(), "text": text})
    return f"Reminder set for {due.isoformat()}: {text}"


def dispatch_tool_call(name, args):
    if name == "remember":
        return tool_remember(args.get("content", ""))
    if name == "recall":
        return tool_recall(args.get("query", ""))
    if name == "remind":
        return tool_remind(int(args.get("minutes", 0)), args.get("text", ""))
    return f"Unknown tool: {name}"


class Assistant:
    def __init__(self):
        self.history = [{"role": "system",
                         "content": "You are a private personal AI assistant with persistent "
                                    "memory. Use the provided tools to remember facts, recall "
                                    "them, and set reminders. Keep replies concise."}]

    def ask(self, user_text):
        self.history.append({"role": "user", "content": user_text})
        try:
            data = _post_chat(self.history, tools=TOOLS)
        except RuntimeError as e:
            return f"[offline] {e}. (Set NEBIUS_API_KEY to enable live Nemotron calls.)"
        choice = data["choices"][0]["message"]
        self.history.append(choice)
        results = []
        for tc in choice.get("tool_calls", []):
            fn = tc.get("function", {})
            try:
                args = json.loads(fn.get("arguments", "{}"))
            except Exception:
                args = {}
            res = dispatch_tool_call(fn.get("name", ""), args)
            results.append(res)
            self.history.append({"role": "tool", "content": res,
                                 "tool_call_id": tc.get("id", "")})
        if results:
            try:
                data2 = _post_chat(self.history, tools=TOOLS)
                reply = data2["choices"][0]["message"]["content"]
                self.history.append({"role": "assistant", "content": reply})
                return reply
            except RuntimeError as e:
                return "\n".join(results) + f"\n[offline final] {e}"
        return choice.get("content", "")


def main():
    a = Assistant()
    print("Nebius Personal AI (type 'exit' to quit). Set NEBIUS_API_KEY to talk to Nemotron.")
    while True:
        try:
            u = input("you> ").strip()
        except EOFError:
            break
        if u.lower() in ("exit", "quit"):
            break
        if not u:
            continue
        print("ai>", a.ask(u))


if __name__ == "__main__":
    main()
