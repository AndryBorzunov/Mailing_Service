from django.contrib import admin
from mailing.models import RecipientMail, Message, Dispatch, Attempt


@admin.register(RecipientMail)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("id", "email_address", "name_fio", "comment", "owner")
    search_fields = ("email_address",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "theme", "body", "owner")
    search_fields = ("theme",)


@admin.register(Dispatch)
class DispatchAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "start_time",
        "end_time",
        "status",
        "message",
        "display_recipients",
        "owner",
    )
    list_filter = ("status", "message")
    search_fields = ("message",)

    def display_recipients(self, obj):
        return ", ".join(
            [recipient.email_address for recipient in obj.recipients.all()]
        )

    display_recipients.short_description = "Recipients"


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "status", "answer", "mailing")
    list_filter = ("created_at", "status", "mailing")
    search_fields = ("mailing",)
