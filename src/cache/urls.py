from baseline.routers import PrefixBasenameSimpleRouter

from .views import CacheViewSet

router = PrefixBasenameSimpleRouter()
router.register(r"caches", CacheViewSet)

urlpatterns = router.urls
