from django.contrib import admin

from .models import Record, Sheet


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'sheet', 'attendant', 'signatary',
        'value', 'operation', 'is_active',
    )
    search_fields = (
        'sheet__merchant__name', 'sheet__merchant__email',
        'sheet__customer__name', 'sheet__customer__email',
        'id',
    )
    autocomplete_fields = (
        'sheet', 'attendant', 'signatary',
    )
    list_filter = (
        'operation', 'is_active',
    )
    ordering = (
        '-created',
    )


@admin.register(Sheet)
class SheetAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'merchant', 'customer', 'is_active',
    )
    search_fields = (
        'merchant__name', 'merchant__email',
        'customer__name', 'customer__email',
    )
    autocomplete_fields = (
        'merchant', 'customer',
    )
    list_filter = (
        'is_active',
    )
    filter_horizontal = (
        'profiles',
    )
    ordering = (
        'merchant__id', 'customer__name',
    )
