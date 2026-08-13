"""
Autentifikatsiya:
1) Telegram Mini App — X-Telegram-Init-Data headeri (HMAC tekshiruvi)
2) Telefon+parol — Authorization: Bearer <token>
"""
import hashlib
import hmac
import json
from urllib.parse import parse_qsl

from django.conf import settings
from rest_framework import authentication, exceptions

from .models import User


def _check_telegram_auth(init_data: str) -> dict:
    if not settings.BOT_TOKEN:
        raise exceptions.AuthenticationFailed("BOT_TOKEN sozlanmagan")

    try:
        parsed = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        raise exceptions.AuthenticationFailed("initData formati noto'g'ri")

    received_hash = parsed.pop("hash", None)
    if not received_hash:
        raise exceptions.AuthenticationFailed("hash topilmadi")

    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))
    secret_key = hmac.new(b"WebAppData", settings.BOT_TOKEN.encode(), hashlib.sha256).digest()
    calculated_hash = hmac.new(
        secret_key, data_check_string.encode(), hashlib.sha256
    ).hexdigest()

    if calculated_hash != received_hash:
        raise exceptions.AuthenticationFailed("Noto'g'ri initData (hash mos kelmadi)")

    return parsed


class TelegramInitDataAuthentication(authentication.BaseAuthentication):
    """`X-Telegram-Init-Data` headeri bo'lsa foydalanuvchini tasdiqlaydi.

    Header bo'lmasa None qaytaradi (anonim so'rov).
    """

    def authenticate(self, request):
        init_data = request.headers.get("X-Telegram-Init-Data")
        if not init_data:
            return None

        parsed = _check_telegram_auth(init_data)
        user_json = json.loads(parsed.get("user", "{}"))

        telegram_id = str(user_json.get("id"))
        if not telegram_id or telegram_id == "None":
            raise exceptions.AuthenticationFailed("Foydalanuvchi ma'lumoti topilmadi")

        user, _ = User.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                "username": user_json.get("username"),
                "full_name": f"{user_json.get('first_name', '')} {user_json.get('last_name', '')}".strip(),
            },
        )

        return (user, None)


class TokenAuthentication(authentication.BaseAuthentication):
    """Authorization: Bearer <token> orqali autentifikatsiya."""

    keyword = "Bearer"

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        parts = auth_header.split()
        if len(parts) != 2 or parts[0] != self.keyword:
            return None

        token = parts[1].strip()
        if not token:
            return None

        try:
            user = User.objects.get(auth_token=token)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("Noto'g'ri yoki muddati o'tgan token")

        return (user, None)
