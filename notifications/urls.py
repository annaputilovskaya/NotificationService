from django.urls import path

from notifications.apps import NotificationsConfig
from notifications.views import NotificationCreateAPIView

app_name = NotificationsConfig.name

urlpatterns = [
    path("create/", NotificationCreateAPIView.as_view(), name="notification-create"),
]
