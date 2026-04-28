from django.contrib import admin

from apps.movements.models import Movement


@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ("description", "movement_type", "value", "date")
    list_filter = ("movement_type", "date")
    search_fields = ("description",)
    ordering = ("-date", "-id")
