from django.contrib import admin

from recipients.models import Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "first_name",
        "last_name",
        "email",
        "phone",
        "tg_chat_id",
    )
