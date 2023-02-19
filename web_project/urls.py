from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# JWT Authentication
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

API_URL_PREFIX = "api"

urlpatterns = [
    path(
        f"{API_URL_PREFIX}/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        f"{API_URL_PREFIX}/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(f"{API_URL_PREFIX}/auth/", include("app_auth.urls", "app_auth")),

    # path('api/password_reset/',
    #      include('django_rest_passwordreset.urls', namespace='password_reset')),

    path("admin/", admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
