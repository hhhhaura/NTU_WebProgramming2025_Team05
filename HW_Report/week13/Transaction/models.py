from django.db import models
from django.contrib.auth.models import User
import string
import random
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def generate_random_slug():
    """Generate a random 10-character string for the slug."""
    characters = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
    return ''.join(random.choice(characters) for _ in range(10))

class Transaction(models.Model):
    creditor = models.ForeignKey(
        User,
        related_name='transactions_given',
        on_delete=models.CASCADE)

    debtor = models.ForeignKey(
        User,
        related_name='transactions_received',
        on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.CharField(
        max_length=10,
        unique=True,
        default=generate_random_slug,
        editable=False  # Prevent manual editing in admin or forms
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.debtor.username} owes {self.creditor.username} ${self.amount}'

    def save(self, *args, **kwargs):
        if not self.slug:
            while True:
                slug = generate_random_slug()
                if not Transaction.objects.filter(slug=slug).exists():
                    self.slug = slug
                    break
        super().save(*args, **kwargs)

        # Broadcast to WebSocket group
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "transactions",
            {
                "type": "transaction_update",
            }
        )