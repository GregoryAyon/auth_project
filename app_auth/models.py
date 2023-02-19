# from django.core.mail import send_mail
# from django_rest_passwordreset.signals import reset_password_token_created
# from django.urls import reverse
# from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
import uuid

# Create your models here.


class User(AbstractUser):
    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Others", "Others"),
    )
    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    gender = models.CharField(
        choices=GENDER_CHOICES, null=True, blank=True, max_length=7
    )
    image = models.ImageField(
        upload_to="profile_picture/%Y/%d/%b", null=True, blank=True
    )

    def save(self, *args, **kwargs):
        self.full_name = self.get_full_name()
        super().save(*args, **kwargs)


class Address(models.Model):
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="user_address",
    )
    attr_id = models.UUIDField(
        unique=True, primary_key=True, default=uuid.uuid4, editable=False
    )
    full_name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    street_address = models.CharField(max_length=50, null=True, blank=True)
    postal_code = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"User{self.user_id}-{self.street_address}"


# @receiver(reset_password_token_created)
# def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

#     email_plaintext_message = "{}?token={}".format(
#         reverse('password_reset:reset-password-request'), reset_password_token.key)

#     send_mail(
#         # title:
#         "Password Reset for {title}".format(title="Some website title"),
#         # message:
#         email_plaintext_message,
#         # from:
#         "noreply@somehost.local",
#         # to:
#         [reset_password_token.user.email]
#     )
