from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.validators import RegexValidator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.URLField(max_length=1024, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    preferred_payment_method = models.CharField(max_length=50, blank=True)
    bank_account = models.CharField(
        max_length=19,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\(\d{3}\)\d{14}$',
                message='Bank account must be in format (XXX)XXXXXXXXXXXXXX, where X are digits',
                code='invalid_bank_account'
            )
        ],
        help_text='Format: (XXX)XXXXXXXXXXXXXX'
    )

    def __str__(self):
        return f"{self.user.username}'s profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('debt', 'New Debt'),
        ('payment', 'Payment Received'),
        ('reminder', 'Payment Reminder'),
        ('system', 'System Message'),
        ('message', 'User Message'),  # New type for user messages
    )

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_notifications')  # New field for message sender
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)
    verification_id = models.IntegerField(null=True, blank=True)  # For storing payment verification IDs
    is_deleted = models.BooleanField(default=False)  # New field to track if notification is deleted

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.notification_type} for {self.recipient.username}: {self.title}"
