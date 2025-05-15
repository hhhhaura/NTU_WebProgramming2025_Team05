from django.contrib import admin
from .models import Transaction

# Register your models here.
class SingleTransaction(admin.ModelAdmin):
  list_display = ("creditor", "debtor", "amount", "description", "created_at", "slug",)
  
admin.site.register(Transaction, SingleTransaction)