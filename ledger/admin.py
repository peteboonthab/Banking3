from django.contrib import admin
from .models import Account, LedgerEntry, AuditLog


admin.site.register(AuditLog)


admin.site.register(Account)
admin.site.register(LedgerEntry) 

# Register your models here.
