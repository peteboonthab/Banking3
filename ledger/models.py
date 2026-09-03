from django.db import models
import uuid


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('TRANSFER', 'Transfer'),
    ]

    user = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    action = models.CharField(
        max_length=50,
        choices=ACTION_CHOICES
    )

    object_type = models.CharField(max_length=50)
    object_id = models.CharField(max_length=100)

    details = models.JSONField(default=dict)

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - {self.user} - {self.created_at}"



class Account(models.Model):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )
    payment_method_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )



    def __str__(self):
        return self.name


class LedgerEntry(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    outflow = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    inflow = models.DecimalField(max_digits=12, decimal_places=2, default=0) 
    created_at = models.DateTimeField(auto_now_add=True)
    idempotency_key = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
        )
    to_account = models.ForeignKey(
    Account,
    on_delete=models.PROTECT,
    related_name='received_entries',
    null=True,
    blank=True
)
    def __str__(self):
        return self.account.name

# Create your models here.
