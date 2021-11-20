from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from knox import views as knox_views
from .views import LibraryViews, RegisterAPI, LoginAPI

# API Open Documentation
schema_view = get_schema_view(
    openapi.Info(
      title="LibraryIS API",
      default_version='v0.1',
      description="API overview for LibraryIS project",
      terms_of_service="",
      contact=openapi.Contact(email="api@iis.czleteron.net"),
      license=openapi.License(name=""),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Authorization & sessions
    path('auth/register/', RegisterAPI.as_view()),
    path('auth/login/', LoginAPI.as_view()),
    path('auth/logout/', knox_views.LogoutView.as_view()),
    path('auth/logoutall/', knox_views.LogoutAllView.as_view()),
    # LibraryIS API
    path('library/', LibraryViews.as_view()),
    path('library/<int:id>', LibraryViews.as_view())
]