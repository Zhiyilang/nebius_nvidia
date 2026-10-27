#!/usr/bin/env python3
"""Minimal stdlib HTTP server exposing the Personal AI assistant as a demo endpoint.

Run:  PORT=8000 python serve.py
Endpoints:
  GET  /            -> health check
  POST /chat        -> {"message": "..."}  ->  {"reply": "..."}
No third-party dependencies.
"""
import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import app as A


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self._send(200, {"status": "ok", "service": "nebius-personal-ai"})

    def do_POST(self):
        if self.path != "/chat":
            self._send(404, {"error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length)
            data = json.loads(raw)
        except Exception:
            self._send(400, {"error": "bad json"})
            return
        a = A.Assistant()
        reply = a.ask(data.get("message", ""))
        self._send(200, {"reply": reply})

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"Serving Personal AI on :{port}")
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()
