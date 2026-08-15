"""
KitobJavon Telegram bot — faqat standart kutubxona (Python 3.14 Windows OK).
"""
import json
import os
import time
import urllib.error
import urllib.request
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
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://book-marketplace-two.vercel.app").strip()

if not BOT_TOKEN or BOT_TOKEN == "SIZNING_BOT_TOKEN":
    raise SystemExit("BOT_TOKEN .env da yo'q. bot/.env ni to'ldiring.")

API = f"https://api.telegram.org/bot{BOT_TOKEN}"


def api(method: str, payload: dict | None = None) -> dict:
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(
        f"{API}/{method}", data=data, headers=headers, method="POST" if data else "GET"
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as res:
            return json.loads(res.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print("API xato:", e.code, body)
        return {}
    except Exception as e:
        print("Tarmoq xato:", e)
        return {}


def send_start(chat_id: int):
    text = (
        "Assalomu alaykum! 👋\n\n"
        "<b>KitobJavon</b> botiga xush kelibsiz.\n"
        "Bu yerda siz:\n"
        "📖 Kitob sotishingiz\n"
        "🔄 Kitob almashtirishingiz\n"
        "📅 Kitob ijaraga berishingiz mumkin\n\n"
        "Boshlash uchun quyidagi tugmani bosing 👇"
    )
    keyboard = {
        "inline_keyboard": [
            [{"text": "📚 KitobJavon — ochish", "web_app": {"url": WEBAPP_URL}}]
        ]
    }
    api(
        "sendMessage",
        {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "reply_markup": keyboard,
        },
    )


def main():
    print("KitobJavon bot ishga tushdi...")
    print("WEBAPP_URL =", WEBAPP_URL)
    offset = 0
    while True:
        res = api("getUpdates", {"offset": offset, "timeout": 30})
        if not res.get("ok"):
            time.sleep(2)
            continue
        for upd in res.get("result", []):
            offset = upd["update_id"] + 1
            msg = upd.get("message") or upd.get("edited_message")
            if not msg:
                continue
            text = (msg.get("text") or "").strip()
            chat_id = msg["chat"]["id"]
            if text.startswith("/start"):
                send_start(chat_id)
                print(" /start ->", chat_id)


if __name__ == "__main__":
    main()