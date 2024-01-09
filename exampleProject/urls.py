from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Documentation API",
        default_version='v0.1',
        description="Documentation API-Example",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="test@test.com"),
        license=openapi.License(name="BSD Licence")
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include('apps.ubigeous.api.urls')),
]

# Swagger Documentation
urlpatterns += [
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]
