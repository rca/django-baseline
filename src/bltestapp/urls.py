from baseline.routers import PrefixBasenameSimpleRouter
from baseline.views.auth import LoginViewSet

from .views import WidgetViewSet

router = PrefixBasenameSimpleRouter()
router.register(r"widgets", WidgetViewSet)
router.register(r"authrrr", LoginViewSet)

urlpatterns = router.urls
