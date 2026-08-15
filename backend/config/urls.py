from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("books.urls")),
    re_path(
        r"^uploads/(?P<path>.*)$",
        serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
]

# Rasm fayllar /uploads/... orqali xizmat qiladi (dev uchun; productionda Nginx/S3 tavsiya etiladi)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
