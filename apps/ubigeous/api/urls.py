from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.ubigeous.api.views import RegionViewSet, ProvinceViewSet, DistrictViewSet, MyTokenObtainPairView, LogoutView, \
    UserViewSet

router = DefaultRouter()

# Routes based on model set views
router.register(r'api/region', RegionViewSet, basename='region')
router.register(r'api/province', ProvinceViewSet, basename='province')
router.register(r'api/district', DistrictViewSet, basename='district')
router.register(r'api/user', UserViewSet, basename='user')

urlpatterns = router.urls

# Authentication
urlpatterns += [
    # JWT Authentication Token
    path('api/auth/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Logout
    path('api/auth/logout/', LogoutView.as_view(), name="logout"),
]
