from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

class CustomUser(AbstractUser):
    USER_ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('member', 'member'),
    ] 
    user_role = models.CharField(max_length=10, choices=USER_ROLE_CHOICES, default='member')

    username = None
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_('First Name'), max_length=255)
    last_name = models.CharField(_('Last Name'), max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    country_code = models.CharField(max_length=4, blank=True, null=True)
    phone_number = PhoneNumberField(_("Phone Number"),region="KE", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email