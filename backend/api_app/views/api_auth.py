from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from knox.models import AuthToken
from api_app.serializers import UserSerializer, LoginSerializer, RegisterSerializer

# ===================================== Register a new account =====================================
"""
    Schema for the possisble responses to registration request
"""
userRegisterResponses = {
    "201": openapi.Response(
        description="Registration Successful.",
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
                },
                "token": "<user_token> # always 64 characters"
            }
        }
    ),
    "400": openapi.Response(
        description="Registration failed",
        examples={
            "application/json": {
                "data": "<error_details>"
            }
        }
    ),
}

"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Authorization"],
    method="POST",
    operation_description="Allows unregistered visitor to create account.",
    request_body=RegisterSerializer,
    responses=userRegisterResponses,
    security=[]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def UserRegistration(request, *args, **kwargs):
    """
        Function that allows users to create an account in the system.
        This function expects correct data in `request.data` -> checked by RegisterSerializer
    """
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    return Response({
        "status": "success",
        "user": UserSerializer(user).data,
        "token": AuthToken.objects.create(user)[1]
    }, status=status.HTTP_201_CREATED)
# ==================================================================================================

# ================================== Login to an existing account ==================================
"""
    Schema for the possisble responses to login request
"""
userLoginResponses = {
    "200": openapi.Response(
        description="Login Success.",
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
                },
                "token": "<user_token> # always 64 characters"
            }
        }
    ),
    "400": openapi.Response(
        description="Login failed!",
        examples={
            "application/json": {
                "non_field_errors": "Invalid details."
            }
        }
    ),
}

"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Authorization"],
    method="POST",
    operation_description="Endpoint for logging in to the system with email and password.",
    request_body=LoginSerializer,
    responses=userLoginResponses,
    security=[]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def UserLogin(request, *args, **kwargs):
    """
        Function that allows users login to an existing account in the system.
        This function expects correct data in `request.data` -> checked by LoginSerializer
    """
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data
    return Response({
        "status": "success",
        "user": UserSerializer(user).data,
        "token": AuthToken.objects.create(user)[1]
    }, status=status.HTTP_200_OK)
# ==================================================================================================