from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "app"

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("accounts/profile/", views.profile, name="profile"),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="logout.html"), name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)