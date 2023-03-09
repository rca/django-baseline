from baseline.routers import PrefixBasenameSimpleRouter
from baseline.views.auth import AuthViewSet

from .views import WidgetViewSet

router = PrefixBasenameSimpleRouter()
router.register(r"widgets", WidgetViewSet)
router.register(r"auth", AuthViewSet)

urlpatterns = router.urls
