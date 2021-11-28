from django.shortcuts import get_object_or_404
from rest_condition import And, Or
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api_app.models import Library, Account, OpeningHours
from api_app.permissions import IsAdministrator, IsLibrarian
from api_app.serializers import LibrarySerializer, OpeningHoursCreateSerializer, UserSerializer

# ==================== List information about all libraries or just selected one ===================
"""
    Schema for the possisble responses to a request for a library information
"""
libraryGetResponses = {
    "200": openapi.Response(
        description="Library information successfully retrieved!",
        examples={
            "application/json": {
                "status": "success",
                "data": [
                    {
                    "id": "<int>",
                    "name": "<string>",
                    "description": "<string>",
                    "city": "<string>",
                    "street": "<string>",
                    "zip_code": "<string> # max 5 characters"
                    }
                ]
            }
        }
    ),
    "404": openapi.Response(
        description="Library was not found!",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    )
}
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Library"],
    method="GET",
    operation_description="Allows users to get list libraries or just display information about selected library",
    responses=libraryGetResponses,
    security=[]
)
@api_view(['GET'])
@permission_classes([AllowAny])
def getLibrary(request, id=None):
    """
        Function that allows users list information about all or just selected libraries.
    """
    if id:
        item = get_object_or_404(Library, pk=id)
        serializer = LibrarySerializer(item)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    items = Library.objects.all()
    serializer = LibrarySerializer(items, many=True)
    return Response({
        "status": "success",
        "data": serializer.data
    }, status=status.HTTP_200_OK)
# ==================================================================================================

# ====================================== Create a new library ======================================
"""
    Schema for the possisble responses to a request for an library create
"""
libraryPostResponses = {
    "200": openapi.Response(
        description="Library successfully created!",
        examples={
            "application/json": {
                "status": "success",
                "data": [
                    {
                    "id": "<int>",
                    "name": "<string>",
                    "description": "<string>",
                    "city": "<string>",
                    "street": "<string>",
                    "zip_code": "<string> # max 5 characters"
                    }
                ]
            }
        }
    ),
    "400": openapi.Response(
        description="Library creation failed!",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    )
}
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Library"],
    method="POST",
    operation_description="Allows user with Administration role to create new library",
    request_body=LibrarySerializer,
    responses=libraryPostResponses
)
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, IsAdministrator)])
def createLibrary(request):
    """
        Function that allows user with an Administrator role to create a new library.
    """
    serializer = LibrarySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "status": "error",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
# ==================================================================================================

# =================================== Update an existing library ===================================
"""
    Schema for the possisble responses to a request for an library edit
"""
libraryPutResponses = {
    "200": openapi.Response(
        description="Library successfully updated!",
        examples={
            "application/json": {
                "status": "success",
                "data": [
                    {
                    "id": "<int>",
                    "name": "<string>",
                    "description": "<string>",
                    "city": "<string>",
                    "street": "<string>",
                    "zip_code": "<string> # max 5 characters"
                    }
                ]
            }
        }
    ),
    "400": openapi.Response(
        description="Library update failed!",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    ),
    "404": openapi.Response(
        description="Library not found!",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    )
}
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Library"],
    method="PUT",
    operation_description="Allows user with Administration or Librarian role to update library",
    request_body=LibrarySerializer,
    responses=libraryPutResponses
)
@api_view(['PUT'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian))])
def updateLibrary(request, id):
    """
        Function that allows user with an Administrator or Librarian role to edit a library.
    """
    library = get_object_or_404(Library, id=id)
    serializer = LibrarySerializer(library, request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "status": "error",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
# ==================================================================================================

# ================================== Add a librarian to a Library ==================================
"""
    Schema for the possisble responses to a request for an association of librarian to a library
"""
libraryPostUserResponse = {
    "200": openapi.Response(
        description="Librarian successfully associated with library!",
        examples={
            "application/json": {
                "status": "success",
                "data": {
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
        description="Selected user is not a librarian!",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    ),
    "404": openapi.Response(
        description="Library or librarian not found!",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    )
}
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Library"],
    method="POST",
    operation_description="Allows user with role Administrator to assign Librarian to a Library",
)
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, IsAdministrator)])
def associateLibrarianToLibrary(request, id, uid):
    """
        Function that allows user with an Administrator role to associate Librarian to a Library.
    """
    library = get_object_or_404(Library, id=id)
    librarian = get_object_or_404(Account, id=uid)
    if librarian.role != '3':
        return Response({
            "status": "error",
            "details": "Selected user is not a Librarian"
        }, status=status.HTTP_400_BAD_REQUEST)
    librarian.working_at = library
    librarian.save()
    return Response({
        "status": "success",
        "data": UserSerializer(librarian).data
    }, status=status.HTTP_200_OK)
# ==================================================================================================

# ================================= Add opening hours to a Library =================================
"""
    Schema for the possisble responses to a request for an association of librarian to a library
"""
libraryPostHoursResponse = {
    "200": openapi.Response(
        description="Opening hours successfully added to a library!",
        examples={
            "application/json": {
                "status": "success"
            }
        }
    ),
    "400": openapi.Response(
        description="Selected user is not a librarian!",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    ),
    "404": openapi.Response(
        description="Library not found!",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    )
}
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Library"],
    method="POST",
    operation_description="Allows user with role Administrator or Librarian to set opening hours",
    request_body=OpeningHoursCreateSerializer,
    responses=libraryPostHoursResponse
)
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian))])
def setOpeningHoursLibrary(request, id):
    """
        Function that allows user with an Administrator or Librarian role to add opening hours to a library.
    """
    library = get_object_or_404(Library, id=id)
    if request.user.role == '3' and request.user.working_at != library:
        return Response({
            "status": "error",
            "details": "Selected user is not a Librarian responsible for this library."
        }, status=status.HTTP_401_UNAUTHORIZED)
    serializer = OpeningHoursCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(library=library)
        return Response({
            "status": "success"
        }, status=status.HTTP_200_OK)
    return Response({
        "status": "error",
        "details": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
# ==================================================================================================

# ================================= Get opening hours to a Library =================================
"""
    Schema for the possisble responses to a request for an association of librarian to a library
"""
libraryGetHoursResponse = {
    "200": openapi.Response(
        description="Opening hours successfully added to a library!",
        examples={
            "application/json": {
                "status": "success",
                "data": {
                    "day": [
                        "<string>"
                    ],
                    "open_time": [
                        "<time>"
                    ],
                    "close_time": [
                        "<time>"
                    ]
                }
            }
        }
    ),
    "400": openapi.Response(
        description="Selected user is not a librarian!",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    ),
    "404": openapi.Response(
        description="Library not found!",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    )
}
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Library"],
    method="GET",
    operation_description="Returns opening hours of the library specified by library id",
    responses=libraryGetHoursResponse
)
@api_view(['GET'])
@permission_classes([AllowAny])
def getOpeningHoursLibrary(request, id):
    """
        Function that allows users to get opening hours of a library.
    """
    item = get_object_or_404(OpeningHours, library=id)
    serializer = OpeningHoursCreateSerializer(item)   
    return Response({
        "status": "success",
        "data": serializer.data
    }, status=status.HTTP_200_OK)
# ==================================================================================================