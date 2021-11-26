from django.urls import path
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from knox import views as knox_views
from .views import UserLogin, UserRegistration, associateLibrarianToLibrary, associatePublicationWithLibrary, createLibrary, createPublication, deleteUser, deleteUserByID, getLibrary, getPublication, getUser, getUserByID, editUser, editUserByID, \
                   getAllUsers, makeAdministrator, makeAdministratorUsingKey, makeDistributor, makeLibrarian, updatePublication, makeRegistredUser

# API Open Documentation
schema_view = get_schema_view(
    openapi.Info(
      title="📚 LibraryIS API",
      default_version='v0.5',
      description="API overview for LibraryIS project",
      terms_of_service="https://iis.czleteron.net/tos/",
      contact=openapi.Contact(name="🏫 IIS Library Project Team", url="https://iis.czleteron.net/team/"),
      license=openapi.License(name="⚖️ MIT License", url="https://iis.czleteron.net/license/"),
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
    # Admin
    path('admin/setrole/administrator/', makeAdministratorUsingKey),
    path('admin/setrole/<int:id>/administrator/', makeAdministrator),
    path('admin/setrole/<int:id>/librarian/', makeLibrarian),
    path('admin/setrole/<int:id>/distributor/', makeDistributor),
    path('admin/setrole/<int:id>/registred/', makeRegistredUser),
    # User
    path('user/', getUser),
    path('user/<int:id>/', getUserByID),
    path('user/edit/', editUser),
    path('user/<int:id>/edit/', editUserByID),
    path('user/delete/', deleteUser),
    path('user/<int:id>/delete/', deleteUserByID),
    path('users/', getAllUsers),
    # Library
    path('library/', getLibrary),
    path('library/<int:id>/', getLibrary),
    path('library/create/', createLibrary),
    path('library/<int:id>/associate/<int:uid>/', associateLibrarianToLibrary),
    # Publication
    path('publication/', getPublication),
    path('publication/<int:id>/', getPublication),
    path('publication/create/', createPublication),
    path('publication/<int:id>/update/', updatePublication),
    path('publication/<int:id>/associate/<int:lid>/', associatePublicationWithLibrary),
    # Order
    path('order/', getOrder),
    path('/order/<int:id>/', getOrder),
    path(/order/library/<int:id>/, getOrderLibrarySpecified),
    path(/order/user/<int:id>/, getOrderUserSpecified),
    path(/order/delivered/<bool:delivered>/, getOrderDelivered),
    path(/order/delivered/<bool:delivered>/library/<int:id>/, getOrderDelivered),
    #path(/order/create/, createOrder),
    path(/order/update/<int:id>/, updateOrder),
    # Book
    #path(/book/, getBook),
    #path(/book/<int:id>/, getBook),
    #path(/book/library/<int:id>/, getBookInLibrary),
    #path(/book/create/, addBook),
    #path(/book/update/<int:id>/, updateBook),
    # Book Loan
    #path(/book_loan/, getLoan),
    #path(/book_loan/<int:id>/, getLoan),
    #path(/book_loan/library/<int:id>/, getLoanInLibrary),
    #path(/book_loan/create/, createLoan),
    #path(/book_loan/create/unregistered/, createLoanUnregistered),
    #path(/book_loan/update/<int:id>/, updateLoan)
]