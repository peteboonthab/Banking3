from django.db import models
import uuid



class Account(models.Model):
    name = models.CharField(max_length=100)
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
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
    def __str__(self):
        return self.account.name

# Create your models here.
