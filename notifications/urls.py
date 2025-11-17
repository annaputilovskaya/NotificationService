from django.urls import path

from notifications.apps import NotificationsConfig
from notifications.views import (
    NotificationCreateAPIView, NotificationListAPIView, NotificationRetrieveAPIView,
)

app_name = NotificationsConfig.name

urlpatterns = [
    path("create/", NotificationCreateAPIView.as_view(), name="create"),
    path("list/", NotificationListAPIView.as_view(), name="list"),
    path("read/", NotificationRetrieveAPIView.as_view(), name="read"),
]
