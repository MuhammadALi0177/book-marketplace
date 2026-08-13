from django.urls import path

from . import views

urlpatterns = [
    path("health", views.HealthView.as_view()),
    path("cities", views.CitiesView.as_view()),
    path("auth/register", views.RegisterView.as_view()),
    path("auth/login", views.LoginView.as_view()),
    path("profile/me", views.ProfileView.as_view()),
    path("profile/password", views.ChangePasswordView.as_view()),
    path("books/mine/list", views.MyBooksView.as_view()),
    path("books", views.BookListCreateView.as_view()),
    path("books/<int:book_id>", views.BookDetailView.as_view()),
    path("upload", views.UploadView.as_view()),
    path("conversations", views.ConversationListCreateView.as_view()),
    path("conversations/<int:conv_id>/messages", views.ConversationMessagesView.as_view()),
]
