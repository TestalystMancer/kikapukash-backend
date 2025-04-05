from django.db import models
from django.conf import settings
from common.models import TimeStampModel
from users.models import CustomUser


# Transaction Model (tracks deposits and withdrawals)


# Notification Model (for sending notifications to users)
class Notification(TimeStampModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user}: {self.message}"
 
