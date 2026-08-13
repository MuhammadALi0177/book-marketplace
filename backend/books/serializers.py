from rest_framework import serializers

from .models import Book, Conversation, Message, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "telegram_id", "username", "full_name", "phone", "city"]


class BookSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
            "city",
            "status",
            "price",
            "description",
            "photo_url",
            "created_at",
            "owner",
        ]


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["title", "author", "city", "status", "price", "description", "photo_url"]


class RegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=32)
    password = serializers.CharField(min_length=4, max_length=128, write_only=True)
    full_name = serializers.CharField(max_length=255, required=False, allow_blank=True)

    def validate_phone(self, value):
        phone = "".join(c for c in value if c.isdigit() or c == "+")
        if len(phone) < 9:
            raise serializers.ValidationError("Telefon raqam noto'g'ri")
        if User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError("Bu telefon raqam allaqachon ro'yxatdan o'tgan")
        return phone

    def create(self, validated_data):
        user = User(
            phone=validated_data["phone"],
            full_name=validated_data.get("full_name") or "",
        )
        user.set_password(validated_data["password"])
        user.generate_token()
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=32)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        phone = "".join(c for c in data["phone"] if c.isdigit() or c == "+")
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError("Telefon yoki parol noto'g'ri")
        if not user.check_password(data["password"]):
            raise serializers.ValidationError("Telefon yoki parol noto'g'ri")
        data["user"] = user
        return data


class MessageSerializer(serializers.ModelSerializer):
    sender_id = serializers.IntegerField(source="sender.id", read_only=True)

    class Meta:
        model = Message
        fields = ["id", "sender_id", "text", "created_at"]


class ConversationSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    other_user = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unread = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            "id",
            "book",
            "other_user",
            "last_message",
            "unread",
            "updated_at",
            "created_at",
        ]

    def get_other_user(self, obj):
        me = self.context["request"].user
        other = obj.seller if obj.buyer_id == me.id else obj.buyer
        return UserSerializer(other).data

    def get_last_message(self, obj):
        msg = obj.messages.order_by("-created_at").first()
        if not msg:
            return None
        return MessageSerializer(msg).data

    def get_unread(self, obj):
        return 0
