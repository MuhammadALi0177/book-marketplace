from django.contrib import admin

from .models import Book, Conversation, Message, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "phone",
        "full_name",
        "username",
        "city",
        "telegram_id",
        "created_at",
    )
    search_fields = ("phone", "telegram_id", "username", "full_name", "city")
    list_filter = ("city",)
    readonly_fields = ("password_hash", "auth_token", "created_at")
    ordering = ("-created_at",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "city",
        "status",
        "price",
        "owner",
        "created_at",
    )
    list_filter = ("status", "city")
    search_fields = ("title", "author", "city", "owner__full_name", "owner__phone")
    autocomplete_fields = ("owner",)
    ordering = ("-created_at",)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "book", "buyer", "seller", "updated_at", "created_at")
    search_fields = (
        "book__title",
        "buyer__full_name",
        "buyer__phone",
        "seller__full_name",
        "seller__phone",
    )
    autocomplete_fields = ("book", "buyer", "seller")
    ordering = ("-updated_at",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "conversation", "sender", "short_text", "created_at")
    search_fields = ("text", "sender__full_name", "sender__phone")
    autocomplete_fields = ("conversation", "sender")
    ordering = ("-created_at",)

    @admin.display(description="Matn")
    def short_text(self, obj):
        t = obj.text or ""
        return t[:60] + ("…" if len(t) > 60 else "")
