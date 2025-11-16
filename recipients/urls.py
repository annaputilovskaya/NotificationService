from rest_framework.routers import SimpleRouter

from recipients.apps import RecipientsConfig
from recipients.views import RecipientViewSet

app_name = RecipientsConfig.name

router = SimpleRouter()
router.register(r"recipients", RecipientViewSet)

urlpatterns = router.urls
