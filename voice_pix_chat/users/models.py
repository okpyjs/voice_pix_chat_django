from basic.models import AutoDate, Plan
from django.contrib.auth.models import AbstractUser
from django.db.models import SET_NULL, BooleanField, CharField, DateTimeField, EmailField, ForeignKey
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from voice_pix_chat.users.managers import UserManager


class User(AbstractUser, AutoDate):
    """
    Default custom user model for Vocie Pix Chat with Automatic Reply by AI.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = CharField(max_length=255, blank=True, null=True)  # type: ignore
    last_name = CharField(max_length=255, blank=True, null=True)  # type: ignore
    email = EmailField(_("email address"), unique=True)
    username = CharField(max_length=255, blank=True, null=True)  # type: ignore

    # custom field
    mail_verify = BooleanField(default=False)
    avatar_url = CharField(max_length=1000, blank=True, null=True)
    plan = ForeignKey(Plan, on_delete=SET_NULL, blank=True, null=True)
    last_seen = DateTimeField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})
