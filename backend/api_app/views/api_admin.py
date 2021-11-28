from django.shortcuts import get_object_or_404
from rest_condition import And
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api_app.models import Account
from api_app.permissions import IsAdministrator
from api_app.serializers import AdminKeySerializer, UserSerializer

"""
    Schema for the possisble responses to a promote request
"""
adminPostResponses = {
    "200": openapi.Response(
        description="User promoted!",
        examples={
            "application/json": {
                "status": "success",
                "user": {
                    "id": "<int>",
                    "email": "<string>",
                    "first_name": "<string>",
                    "last_name": "<string>",
                    "city": "<string>",
                    "street": "<string>",
                    "zip_code": "<string> # max 5 characters",
                    "country": "<string>",
                    "phone": "<null>",
                    "role": "<int> # admin(4), librarian(3), distributor(2), registred(1), unregistred(0)",
                    "working_at": "<null>",
                    "date_joined": "<date_time>",
                    "last_login": "<date_time>"
                }
            }
        }
    ),
    "400": openapi.Response(
        description="Bad Request.",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    ),
    "401": openapi.Response(
        description="Unauthorized to get user details or promote user!",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    ),
    "404": openapi.Response(
        description="User not found!",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    )
}
# =========================== Self-promote user account to Administrator ===========================
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Administration"],
    method="POST",
    operation_description="Allows user to promote himself to an Administrator if no other Administrator is defined yet",
    request_body=AdminKeySerializer,
    responses=adminPostResponses
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def makeAdministratorUsingKey(request):
    """
        Function that allows user to promote himself to an Administrator.
        This function expects user to be logged in. If there is already an Administrator defined
        the function will fail.
    """
    try:
        admin = Account.objects.get(role='4')
    except:
        pass
    else:
        if admin:
            return Response({
                "status": "error",
                "data": "Another Administrator already exists.",
            }, status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(Account, email=request.user.email)
    serializer = AdminKeySerializer(data=request.data)
    if serializer.is_valid() is not True:
        return Response({
            "status": "error",
            "data": "Invalid key!"
        }, status=status.HTTP_401_UNAUTHORIZED)
    user.role = '4'
    user.save()
    return Response({
        "status": "success",
        "data": UserSerializer(user).data
    }, status=status.HTTP_200_OK)
# ==================================================================================================

# ============================ Promote a user account to Administrator =============================
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Administration"],
    method="POST",
    operation_description="Allows users with Administrator role to change selected user's role to an Administrator",
    responses=adminPostResponses
)
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, IsAdministrator)])
def makeAdministrator(request, id):
    """
        Function that allows Administrator to promote a user to an Administrator.
        This function expects user that is logged in to be an Administrator.
    """
    user = get_object_or_404(Account, id=id)
    user.role = '4'
    user.save()
    return Response({
        "status": "success",
        "data": UserSerializer(user).data
    }, status=status.HTTP_200_OK)
# ==================================================================================================

# ============================== Promote a user account to Librarian ===============================
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Administration"],
    method="POST",
    operation_description="Allows users with Administrator role to change selected user's role to Librarian",
    responses=adminPostResponses
)
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, IsAdministrator)])
def makeLibrarian(request, id):
    """
        Function that allows Administrator to promote a user to a Librarian.
        This function expects user that is logged in to be an Administrator.
    """
    user = get_object_or_404(Account, id=id)
    user.role = '3'
    user.save()
    return Response({
        "status": "success",
        "data": UserSerializer(user).data
    }, status=status.HTTP_200_OK)
# ==================================================================================================

# ============================= Promote a user account to Distributor ==============================
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Administration"],
    method="POST",
    operation_description="Allows users with Administrator role to change selected user's role to Distributor",
    responses=adminPostResponses
)
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, IsAdministrator)])
def makeDistributor(request, id):
    """
        Function that allows Administrator to promote a user to a Distributor.
        This function expects user that is logged in to be an Administrator.
    """
    user = get_object_or_404(Account, id=id)
    user.role = '2'
    user.save()
    return Response({
        "status": "success",
        "data": UserSerializer(user).data
    }, status=status.HTTP_200_OK)
# ==================================================================================================

# =========================== Promote a user account to Registred User =============================
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Administration"],
    method="POST",
    operation_description="Allows users with Administrator role to change selected user's role to Registred User",
    responses=adminPostResponses
)
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, IsAdministrator)])
def makeRegistredUser(request, id):
    """
        Function that allows Administrator to promote a user to a Registred User.
        This function expects user that is logged in to be an Administrator.
    """
    user = get_object_or_404(Account, id=id)
    user.role = '1'
    user.save()
    return Response({
        "status": "success",
        "data": UserSerializer(user).data
    }, status=status.HTTP_200_OK)
# ==================================================================================================