from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'scope', 'max_usage', 'usage', 'expire_in'
    )
    search_fields = (
        'id',
    )
    list_filter = (
        'scope', 'expire_in',
    )
    ordering = (
        '-created',
    )
