from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.TextField()  # The content of the notification
    is_read = models.BooleanField(default=False)  # Whether the notification has been read
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the notification was created

    def __str__(self):
        return f"Notification for {self.user} - {self.created_at}"

    class Meta:
        ordering = ['-created_at']  # Show latest notifications first
