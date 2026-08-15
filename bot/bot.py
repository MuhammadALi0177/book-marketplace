"""KitobJavon bot — Render Web Service (PORT + polling)."""
import json
import os
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path


def load_env():
    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


load_env()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
WEBAPP_URL = os.getenv(
    "WEBAPP_URL", "https://book-marketplace-two.vercel.app"
).strip()
PORT = int(os.environ.get("PORT", "10000"))

if not BOT_TOKEN:
    raise SystemExit("BOT_TOKEN environment variable required")

API = f"https://api.telegram.org/bot{BOT_TOKEN}"


def api(method, payload=None):
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(
        f"{API}/{method}",
        data=data,
        headers=headers,
        method="POST" if data else "GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as res:
            return json.loads(res.read().decode("utf-8"))
    except Exception as e:
        print("api error:", e)
        return {}


def send_start(chat_id):
    api(
        "sendMessage",
        {
            "chat_id": chat_id,
            "text": (
                "Assalomu alaykum! 👋\n\n"
                "<b>KitobJavon</b> botiga xush kelibsiz.\n"
                "Boshlash uchun tugmani bosing 👇"
            ),
            "parse_mode": "HTML",
            "reply_markup": {
                "inline_keyboard": [
                    [
                        {
                            "text": "📚 KitobJavon — ochish",
                            "web_app": {"url": WEBAPP_URL},
                        }
                    ]
                ]
            },
        },
    )


def poll_loop():
    print("polling... WEBAPP_URL=", WEBAPP_URL, flush=True)
    offset = 0
    while True:
        res = api("getUpdates", {"offset": offset, "timeout": 30})
        if not res.get("ok"):
            time.sleep(3)
            continue
        for upd in res.get("result", []):
            offset = upd["update_id"] + 1
            msg = upd.get("message") or upd.get("edited_message")
            if not msg:
                continue
            text = (msg.get("text") or "").strip()
            if text.startswith("/start"):
                send_start(msg["chat"]["id"])
                print("/start", msg["chat"]["id"], flush=True)


class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"ok"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    print(f"binding 0.0.0.0:{PORT}", flush=True)
    server = HTTPServer(("0.0.0.0", PORT), HealthHandler)
    threading.Thread(target=poll_loop, daemon=True).start()
    server.serve_forever()