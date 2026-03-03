from django.urls import path
from django.views.decorators.cache import cache_page

import mailing.views
from mailing.apps import MailingConfig
from mailing.views import DispatchListView, DispatchDetailView, DispatchCreateView, DispatchUpdateView, \
    DispatchDeleteView, RecipientMailListView, RecipientMailDetailView, RecipientMailCreateView, \
    RecipientMailUpdateView, RecipientMailDeleteView, MailingSummaryView, MessageListView, MessageDetailView, \
    MessageCreateView, MessageUpdateView, MessageDeleteView, AttemptListView

app_name = MailingConfig.name


urlpatterns = [
    path("", MailingSummaryView.as_view(), name="mailing_summary"),
    path("process_command/", mailing.views.process_command, name="process_command"),
    path("mailings/", DispatchListView.as_view(), name='dispatch_list'),
    path(
        "mailing/<int:pk>/",
        cache_page(60)(DispatchDetailView.as_view()),
        name="dispatch_detail"
    ),
    path("dispatch/create/", DispatchCreateView.as_view(), name="dispatch_create"),
    path("dispatch/<int:pk>/update/", DispatchUpdateView.as_view(), name="dispatch_update"),
    path("dispatch/<int:pk>/delete/", DispatchDeleteView.as_view(), name="dispatch_delete"),
    path("recipient_mails/", RecipientMailListView.as_view(), name="recipient_mails"),
    path(
        "recipientmail/<int:pk>/",
        cache_page(60)(RecipientMailDetailView.as_view()),
        name="recipientmail_detail"
    ),
    path("recipient_mails/create/", RecipientMailCreateView.as_view(), name="recipientmail_create"),
    path("recipientmail/<int:pk>/update/", RecipientMailUpdateView.as_view(), name="recipientmail_update"),
    path("recipientmail/<int:pk>/delete/", RecipientMailDeleteView.as_view(), name="recipientmail_delete"),
    path("messages/", MessageListView.as_view(), name="message_list"),
    path("message/<int:pk>/", cache_page(60)(MessageDetailView.as_view()), name="message_detail"),
    path("message/create/", MessageCreateView.as_view(), name="message_create"),
    path("message/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"),
    path("message/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"),
    path("attempts/", AttemptListView.as_view(), name="attempt_list")
]
