from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import DispatchListView, DispatchDetailView, DispatchCreateView, DispatchUpdateView, \
    DispatchDeleteView

app_name = MailingConfig.name

urlpatterns = [
    path("", DispatchListView.as_view(), name='dispatch_list'),
    path(
        "mailing/<int:pk>/",
        DispatchDetailView.as_view(),
        name="dispatch_detail"
    ),
    path("dispatch/create/", DispatchCreateView.as_view(), name="dispatch_create"),
    path("dispatch/<int:pk>/update/", DispatchUpdateView.as_view(), name="dispatch_update"),
    path("dispatch/<int:pk>/delete/", DispatchDeleteView.as_view(), name="dispatch_delete")
]
