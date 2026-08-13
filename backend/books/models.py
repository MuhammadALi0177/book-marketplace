from django.db import models


class User(models.Model):
    """Foydalanuvchi: Telegram yoki telefon+parol orqali autentifikatsiya."""

    telegram_id = models.CharField(
        max_length=64, unique=True, null=True, blank=True, db_index=True
    )
    username = models.CharField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(
        max_length=32, unique=True, null=True, blank=True, db_index=True
    )
    password_hash = models.CharField(max_length=128, null=True, blank=True)
    auth_token = models.CharField(
        max_length=64, unique=True, null=True, blank=True, db_index=True
    )
    city = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # DRF permission (IsAuthenticated) shu atributni tekshiradi
    @property
    def is_authenticated(self):
        return True

    def set_password(self, raw_password: str):
        from django.contrib.auth.hashers import make_password

        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password: str) -> bool:
        from django.contrib.auth.hashers import check_password

        if not self.password_hash:
            return False
        return check_password(raw_password, self.password_hash)

    def generate_token(self) -> str:
        import secrets

        self.auth_token = secrets.token_hex(32)
        return self.auth_token

    def __str__(self):
        return (
            self.username
            or self.full_name
            or self.phone
            or self.telegram_id
            or str(self.pk)
        )


class BookStatus(models.TextChoices):
    SALE = "sale", "Sotish"
    RENT = "rent", "Ijara"
    BARTER = "barter", "Almashtirish"


class Book(models.Model):
    owner = models.ForeignKey(User, related_name="books", on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    city = models.CharField(max_length=255, db_index=True)
    status = models.CharField(
        max_length=10, choices=BookStatus.choices, db_index=True
    )
    price = models.FloatField(null=True, blank=True)  # barter bo'lsa null bo'lishi mumkin
    description = models.TextField(null=True, blank=True)
    photo_url = models.CharField(max_length=500, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.author})"



class Conversation(models.Model):
    """Ikki foydalanuvchi o'rtasidagi suhbat (kitob haqida)."""
    book = models.ForeignKey(Book, related_name="conversations", on_delete=models.CASCADE, null=True, blank=True)
    buyer = models.ForeignKey(User, related_name="conversations_as_buyer", on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name="conversations_as_seller", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        unique_together = [("book", "buyer", "seller")]

    def __str__(self):
        return f"Conv #{self.pk}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Msg #{self.pk}"
