import os
import uuid
import base64

from django.conf import settings
from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Book, BookStatus, Conversation, Message, User
from .serializers import (
    BookCreateSerializer,
    BookSerializer,
    ConversationSerializer,
    LoginSerializer,
    MessageSerializer,
    RegisterSerializer,
    UserSerializer,
)

# Asosiy O'zbekiston shaharlari/viloyatlari — kerak bo'lsa DB'ga o'tkazish mumkin
UZ_CITIES = [
    "Toshkent", "Toshkent viloyati", "Andijon", "Namangan", "Farg'ona", "Qo'qon",
    "Marg'ilon", "Samarqand", "Buxoro", "Navoiy", "Jizzax", "Sirdaryo",
    "Qarshi", "Termiz", "Urganch", "Nukus", "Angren", "Chirchiq", "Olmaliq",
    "Guliston", "Denov", "Zarafshon", "Katakurgan", "Shahrisabz",
]

ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif", ".gif"}


class HealthView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"status": "ok"})


class CitiesView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response(UZ_CITIES)


class RegisterView(APIView):
    """Telefon + parol bilan ro'yxatdan o'tish."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "token": user.auth_token,
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """Telefon + parol bilan kirish."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        if not user.auth_token:
            user.generate_token()
            user.save(update_fields=["auth_token"])
        return Response(
            {
                "token": user.auth_token,
                "user": UserSerializer(user).data,
            }
        )


class ProfileView(APIView):
    """Joriy foydalanuvchining sotuvchi profili."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        user = request.user
        for field in ("full_name", "phone", "city"):
            value = request.data.get(field)
            if value:
                setattr(user, field, value)
        user.save(update_fields=["full_name", "phone", "city"])
        return Response(UserSerializer(user).data)



class ChangePasswordView(APIView):
    """Parolni yangilash: {password}"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        password = request.data.get("password") or ""
        if len(password) < 4:
            return Response(
                {"detail": "Parol kamida 4 belgi bo'lishi kerak"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = request.user
        user.set_password(password)
        user.save(update_fields=["password_hash"])
        return Response({"ok": True})


class BookListCreateView(generics.ListCreateAPIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BookCreateSerializer
        return BookSerializer

    def get_queryset(self):
        qs = Book.objects.select_related("owner").all()

        city = self.request.query_params.get("city")
        book_status = self.request.query_params.get("status")
        search = self.request.query_params.get("search")

        if city:
            qs = qs.filter(city__icontains=city)
        if book_status:
            qs = qs.filter(status=book_status)
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(author__icontains=search))

        return qs.order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        if not getattr(request.user, "phone", None):
            return Response(
                {"detail": "Avval sotuvchi profilingizni to'ldiring: telefon raqam kerak."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        book = serializer.instance
        return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)


class BookDetailView(generics.RetrieveDestroyAPIView):
    queryset = Book.objects.select_related("owner").all()
    serializer_class = BookSerializer
    lookup_url_kwarg = "book_id"

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_destroy(self, instance):
        if instance.owner_id != self.request.user.id:
            raise PermissionDenied("Ruxsat yo'q")
        instance.delete()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"ok": True})


class MyBooksView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            Book.objects.select_related("owner")
            .filter(owner=self.request.user)
            .order_by("-created_at")
        )


class UploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        file = request.FILES.get("file") or request.FILES.get("image")
        if not file:
            return Response({"detail": "Fayl topilmadi"}, status=status.HTTP_400_BAD_REQUEST)

        ext = os.path.splitext(file.name)[1].lower()
        if not ext:
            ext = ".jpg"
        if ext not in ALLOWED_EXT:
            return Response(
                {"detail": "Faqat jpg/png/webp rasm qabul qilinadi"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        filename = f"{uuid.uuid4().hex}{ext}"
        filepath = os.path.join(settings.MEDIA_ROOT, filename)

        with open(filepath, "wb") as f:
            for chunk in file.chunks():
                f.write(chunk)

        return Response({"photo_url": f"{settings.MEDIA_URL}{filename}"})



class ConversationListCreateView(APIView):
    """Foydalanuvchi suhbatlari ro'yxati va yangi suhbat ochish."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = (
            Conversation.objects.filter(Q(buyer=request.user) | Q(seller=request.user))
            .select_related("book", "book__owner", "buyer", "seller")
            .prefetch_related("messages")
        )
        data = ConversationSerializer(qs, many=True, context={"request": request}).data
        return Response(data)

    def post(self, request):
        """Yangi suhbat: {book_id} — kitob egasi bilan yozishma."""
        book_id = request.data.get("book_id")
        if not book_id:
            return Response({"detail": "book_id kerak"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            book = Book.objects.select_related("owner").get(pk=book_id)
        except Book.DoesNotExist:
            return Response({"detail": "Kitob topilmadi"}, status=status.HTTP_404_NOT_FOUND)

        if book.owner_id == request.user.id:
            return Response(
                {"detail": "O'z e'loningizga yozolmaysiz"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        conv, _ = Conversation.objects.get_or_create(
            book=book,
            buyer=request.user,
            seller=book.owner,
        )
        data = ConversationSerializer(conv, context={"request": request}).data
        return Response(data, status=status.HTTP_201_CREATED)


class ConversationMessagesView(APIView):
    """Suhbat xabarlari: GET ro'yxat, POST yangi xabar."""

    permission_classes = [permissions.IsAuthenticated]

    def _get_conv(self, request, conv_id):
        try:
            conv = Conversation.objects.select_related("buyer", "seller", "book").get(pk=conv_id)
        except Conversation.DoesNotExist:
            return None
        if request.user.id not in (conv.buyer_id, conv.seller_id):
            return None
        return conv

    def get(self, request, conv_id):
        conv = self._get_conv(request, conv_id)
        if not conv:
            return Response({"detail": "Topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        msgs = conv.messages.select_related("sender").all()
        return Response(MessageSerializer(msgs, many=True).data)

    def post(self, request, conv_id):
        conv = self._get_conv(request, conv_id)
        if not conv:
            return Response({"detail": "Topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        text = (request.data.get("text") or "").strip()
        if not text:
            return Response({"detail": "Xabar matni bo'sh"}, status=status.HTTP_400_BAD_REQUEST)
        msg = Message.objects.create(conversation=conv, sender=request.user, text=text)
        conv.save(update_fields=["updated_at"])  # touch updated_at
        return Response(MessageSerializer(msg).data, status=status.HTTP_201_CREATED)
