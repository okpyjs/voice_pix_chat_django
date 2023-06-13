from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from voice_pix_chat.chat.api.views import TestViewSet
from voice_pix_chat.users.api.views import (
    LoginView,
    LogoutView,
    MailVerify,
    RegisterView,
    ReSendMailVerifyCodeView,
    UserViewSet,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
# router.register("login", TestViewSet, basename="login")

api_urls = [
    path("login/", view=LoginView.as_view(), name="login"),
    path("register/", view=RegisterView.as_view(), name="register"),
    path("mail-verify/", view=MailVerify.as_view(), name="mail-verify"),
    path("resend-mail-verify/", view=ReSendMailVerifyCodeView.as_view(), name="resend-mail-verify"),
    path("logout/", view=LogoutView.as_view(), name="logout"),
]


app_name = "api"
urlpatterns = router.urls + api_urls
