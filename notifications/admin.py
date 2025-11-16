from django.contrib import admin

from notifications.models import Notification


class RecipientInline(admin.TabularInline):
    model = Notification.recipients.through


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "topic",
        "text",
        "status",
    )
    inlines = [RecipientInline]
