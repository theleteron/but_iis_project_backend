from django.urls import path
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from knox import views as knox_views
from .views import UserLogin, UserRegistration, associateLibrarianToLibrary, createLibrary, createPublication, deleteUser, deleteUserByID, getLibrary, getPublication, getUser, getUserByID, editUser, editUserByID, \
                   getAllUsers

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
   #url='https://iis.czleteron.net/api/',
   public=True,
   permission_classes=[permissions.AllowAny],
)

# Swagger custom override
logoutResponse = {
    "204": openapi.Response(
        description="Logout Successfull."
    ),
    "401": openapi.Response(
        description="Unauthorized. Invalid token.",
        examples={
            "application/json": {
                "detail": "Authentication credentials were not provided."
            }
        }
    ),
}
knox_logout = swagger_auto_schema(
    tags=["Authorization"], 
    method="POST",
    operation_description="Endpoint for logging out of the system.",
    responses=logoutResponse
) (knox_views.LogoutView.as_view())
knox_logoutAll = swagger_auto_schema(
    tags=["Authorization"], 
    method="POST",
    operation_description="Endpoint for logging out of the system. Logs out of all devices!",
    responses=logoutResponse
) (knox_views.LogoutAllView.as_view())

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('doc/swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('doc/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Authorization
    path('auth/login/', UserLogin),
    path('auth/logout/', knox_logout),
    path('auth/logoutall/', knox_logoutAll),
    path('auth/register/', UserRegistration),
    # User
    path('user/', getUser),
    path('user/<int:id>/', getUserByID),
    path('user/edit/', editUser),
    path('user/edit/<int:id>/', editUserByID),
    path('user/delete/', deleteUser),
    path('user/delete/<int:id>/', deleteUserByID),
    path('users/', getAllUsers),
    # Library
    path('library/', getLibrary),
    path('library/<int:id>/', getLibrary),
    path('library/create/', createLibrary),
    path('library/<int:id>/associate/<int:uid>/', associateLibrarianToLibrary),
    # Publication
    path('publication/', getPublication),
    path('publication/<int:id>/', getPublication),
    path('publication/create/', createPublication)
]