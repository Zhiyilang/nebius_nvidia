#!/usr/bin/env python3
"""Self-check for the Nebius Personal AI assistant.

Verifies the parts that run WITHOUT a live API key:
  - persistent memory round-trip (remember / recall)
  - reminder scheduling
  - safe tool dispatch
  - graceful offline behaviour when NEBIUS_API_KEY is absent
  - sane default configuration

The live Nemotron call is intentionally NOT asserted here: it requires the
user's Nebius API key. That path is exercised manually after key setup.
Exit code 0 = all local checks passed.
"""
import os
import sys
import tempfile

# Force a temp memory file BEFORE importing app (app reads MEMORY_PATH at import).
tmp = tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False)
tmp.close()
os.environ["MEMORY_PATH"] = tmp.name
os.environ.pop("NEBIUS_API_KEY", None)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app as A

fails = []


def check(name, cond):
    print(("PASS" if cond else "FAIL") + " - " + name)
    if not cond:
        fails.append(name)


# 1. remember writes to the store
A.tool_remember("User prefers the red team over the blue team.")
check("remember writes to store", os.path.getsize(tmp.name) > 0)

# 2. recall finds the stored fact
r2 = A.tool_recall("red team")
check("recall finds stored fact", "red team" in r2)

# 3. remind stores a future reminder
r3 = A.tool_remind(30, "Stand-up meeting")
check("remind stores reminder", "Stand-up meeting" in r3)

# 4. unknown tool is handled safely
check("unknown tool safe", "Unknown tool" in A.dispatch_tool_call("nope", {}))

# 5. offline ask degrades gracefully without a key
a = A.Assistant()
out = a.ask("Remember I like tea.")
check("offline ask graceful", "[offline]" in out)

# 6. configuration defaults are sane
check("default model set", bool(A.MODEL))
check("base url points at nebius", "nebius.com" in A.BASE_URL)
check("tool schema has 3 skills", len(A.TOOLS) == 3)

os.unlink(tmp.name)
if fails:
    print("FAILED:", fails)
    sys.exit(1)
print("ALL CHECKS PASSED")
sys.exit(0)
