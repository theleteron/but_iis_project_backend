from django.shortcuts import get_object_or_404
from django.contrib.auth.signals import user_logged_out
from rest_condition import And, Or
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api_app.models import Account
from api_app.permissions import IsAdministrator, IsLibrarian
from api_app.serializers import UserSerializer, UserNormalEditSerializer, UserAdminEditSerializer

"""
    Schema for the possisble responses to a request for an user information
"""
userGetResponses = {
    "200": openapi.Response(
        description="Retrieval of user information OK.",
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
                    "role": "<int> # admin(4), librarian(3), distributor(2), registered(1), unregistered(0)",
                    "working_at": "<null>",
                    "date_joined": "<date_time>",
                    "last_login": "<date_time>"
                }
            }
        }
    ),
    "401": openapi.Response(
        description="Unauthorized to get user details!",
        examples={
            "application/json": {
                "detail": "Authentication credentials were not provided."
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
# ========================= Get information about currently logged in user =========================
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["User"],
    method="GET",
    operation_description="Allows user to get his own information",
    responses=userGetResponses
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUser(request):
    """
        Function that allows user to get information about himself.
        This function expects user to be logged in.
    """
    return Response({
        "status": "success",
        "user": UserSerializer(request.user).data
    }, status=status.HTTP_200_OK)
# ==================================================================================================

# ============================== Get information about a specific user =============================
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["User"],
    method="GET",
    operation_description="Allows user with role of Administrator or Librarian to get information about specified user",
    responses=userGetResponses
)
@api_view(['GET'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian))])
def getUserByID(request, id):
    """
        Function that allows user with a Administrator or Librarian role to get information about user.
        This function expects user to be logged in and have required roles.
    """
    user = get_object_or_404(Account, pk=id)
    return Response({
        "status": "success",
        "user": UserSerializer(user).data
    }, status=status.HTTP_200_OK)
# ==================================================================================================

"""
    Schema for the possisble responses to a request for user edit
"""
userPutResponses = {
    "200": openapi.Response(
        description="User updated!",
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
                    "role": "<int> # admin(4), librarian(3), distributor(2), registered(1), unregistered(0)",
                    "working_at": "<null>",
                    "date_joined": "<date_time>",
                    "last_login": "<date_time>"
                }
            }
        }
    ),
    "400": openapi.Response(
        description="Invalid data format.",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    ),
    "401": openapi.Response(
        description="Unauthorized to get user details",
        examples={
            "application/json": {
                "detail": "Authentication credentials were not provided."
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
# ========================= Edit information of a currently logged in user =========================
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["User"],
    method="PUT",
    operation_description="Allows user to edit his own informations",
    request_body=UserNormalEditSerializer,
    responses=userPutResponses
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def editUser(request):
    """
        Function that allows user to modify his own information.
        This function expects user to be logged in.
    """
    user = get_object_or_404(Account, email=request.user.email)
    serializer = UserNormalEditSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": "success",
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    return Response({
        "status": "error",
        "data": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
# ==================================================================================================

# =============================== Edit information of a specific user ==============================
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["User"],
    method="PUT",
    operation_description="Allows user with Administrator role edit other users",
    request_body=UserAdminEditSerializer,
    responses=userPutResponses
)
@api_view(['PUT'])
@permission_classes([And(IsAuthenticated, IsAdministrator)])
def editUserByID(request, id):
    """
        Function that allows user with a Administrator role to modify information of a user.
        This function expects user to be logged in and have required roles.
    """
    user = get_object_or_404(Account, id=id)
    serializer = UserAdminEditSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": "success",
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    return Response({
        "status": "error",
        "data": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
# ==================================================================================================

"""
    Schema for the possisble responses to a request for user delete
"""
userDeleteResponses = {
    "200": openapi.Response(
        description="User deleted!",
        examples={
            "application/json": {
                "status": "success"
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
        description="Unauthorized to get user details!",
        examples={
            "application/json": {
                "detail": "Authentication credentials were not provided."
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
# ===================================== Delete a logged in user ====================================
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["User"],
    method="DELETE",
    operation_description="Deletes user",
    responses=userDeleteResponses
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteUser(request):
    """
        Function that allows user to delete himself.
        This function expects user to be logged in.
        Warning! Doesn't delete user but just deactivates him!
    """
    user = get_object_or_404(Account, email=request.user.email)
    if user is None:
        return Response({
            "status": "error",
            "data": "Failed to delete user.",
        }, status=status.HTTP_400_BAD_REQUEST)
    user.is_active = False
    user.save()
    user.auth_token_set.all().delete()
    user_logged_out.send(sender=user.__class__,
                         request=request, user=user)
    return Response({
        "status": "success"
    }, status=status.HTTP_200_OK)
# ==================================================================================================

# ===================================== Delete a specific user =====================================
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["User"],
    method="DELETE",
    operation_description="Allows user with Administrator permission to delete specified user",
    responses=userDeleteResponses
)
@api_view(['DELETE'])
@permission_classes([And(IsAuthenticated, IsAdministrator)])
def deleteUserByID(request, id):
    """
        Function that allows user with an Administrator role to delete specified user.
        This function expects user to be logged in and have required roles.
        Warning! Doesn't delete user but just deactivates him!
    """
    user = get_object_or_404(Account, id=id)
    if user is None:
        return Response({
            "status": "error",
            "data": "Failed to delete user.",
        }, status=status.HTTP_400_BAD_REQUEST)
    user.is_active = False
    user.save()
    user.auth_token_set.all().delete()
    user_logged_out.send(sender=user.__class__, user=user)
    return Response({
        "status": "success"
    }, status=status.HTTP_200_OK)
# ==================================================================================================

# ===================================== Get list of all users ======================================
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["User"],
    method="GET",
    operation_description="Lists all users from the system",
    responses=userGetResponses
)
@api_view(['GET'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian))])
def getAllUsers(request):
    """
        Function that allows user with an Administrator or Librarian role to list all users.
        This function expects user to be logged in and have required roles.
    """
    users = Account.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response({
        "status": "success",
        "data": serializer.data
    }, status=status.HTTP_200_OK)
# ==================================================================================================