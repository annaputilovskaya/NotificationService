from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Notification Service API",
        default_version="v1",
        description=(
            "API сервиса доставки уведомлений по каналам "
            "Email → Telegram → SMS с автоматическим failover."
        ),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[
        permissions.AllowAny,
    ],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("users/", include("users.urls", namespace="users")),
    path("", include("recipients.urls", namespace="recipients")),
    path(
        "notifications/",
        include("notifications.urls", namespace="notifications"),
    ),
]
