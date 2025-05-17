from django.contrib import admin
from .models import Transaction, SharedExpense, ExpenseShare

class ExpenseShareInline(admin.TabularInline):
    model = ExpenseShare
    extra = 1

class SharedExpenseAdmin(admin.ModelAdmin):
    list_display = ("paid_by", "amount", "description", "created_at", "slug")
    inlines = [ExpenseShareInline]
    search_fields = ("paid_by__username", "description")
    list_filter = ("created_at",)

class SingleTransaction(admin.ModelAdmin):
    list_display = ("creditor", "debtor", "amount", "description", "created_at", "slug")
    search_fields = ("creditor__username", "debtor__username", "description")
    list_filter = ("created_at",)

admin.site.register(SharedExpense, SharedExpenseAdmin)
admin.site.register(Transaction, SingleTransaction)
admin.site.register(ExpenseShare)