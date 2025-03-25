from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):
    """
    Custom User model extending AbstractUser with a mobile field.
    """

    mobile = models.CharField(max_length=15, unique=True)

    # Resolve conflicts with Django's built-in User model
    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

    def __str__(self):
        return self.username


class Task(models.Model):
    """
    Task model that supports multiple users with ManyToManyField.
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    name = models.CharField(max_length=255,unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    task_type = models.CharField(max_length=250, default='task')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_user = models.ManyToManyField(User, related_name='assigned_tasks')

    class Meta:
        verbose_name_plural = "Tasks"
        ordering = ["-created_at"]  # Latest tasks appear first

    def save(self, *args, **kwargs):
        """
        Auto-update completed_at when status is changed to 'completed'.
        """
        if self.status == "completed" and not self.completed_at:
            self.completed_at = now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.status} - {self.created_at.strftime('%Y-%m-%d')}"
