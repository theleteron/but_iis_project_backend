from django.shortcuts import get_object_or_404
from rest_condition import And, Or
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api_app.models import Book
from api_app.permissions import IsAdministrator, IsLibrarian
from api_app.serializers import BookSerializer

"""
    Schema for the possisble responses to a request for a book information
"""
bookGetResponses = {
    "200": openapi.Response(
        description="Book information retrieved successfully!",
        examples={
            "application/json": {
                "status": "success",
                "data": [
                    {
                        "id": "<int>",
                        "publication": "<int>",
                        "library": "<int>",
                        "condition": "<string>",
                        "section": "<int>",
                        "loaned": "<boolean>",
                        "reserved": "<boolean>"
                    }
                ]
            }
        }
    ),
    "404": openapi.Response(
        description="Book not found!",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    )
}
# =================== List information about all books or just the one specified ===================
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Book"],
    method="GET",
    operation_description="Returns list of all books in the system or just selected one!",
    responses=bookGetResponses,
    security=[]
)
@api_view(['GET'])
@permission_classes([AllowAny])
def getBook(request, id=None):
    """
        Function that allows users to list all books or just one specified.
    """
    if id:
        item = get_object_or_404(Book, pk=id)
        serializer = BookSerializer(item)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    items = Book.objects.all()
    serializer = BookSerializer(items, many=True)
    return Response({
        "status": "success",
        "data": serializer.data
    }, status=status.HTTP_200_OK)
# ==================================================================================================

# ====================== List information about all books in specified library =====================
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Book"],
    method="GET",
    operation_description="Returns list of all books in the system in the library specified by library id",
    responses=bookGetResponses,
    security=[]
)
@api_view(['GET'])
@permission_classes([AllowAny])
def getBookInLibrary(request, id):
    """
        Function that allows users to list all books in specified library.
    """
    items = Book.objects.filter(library=id)
    if not items:
        return Response({
            "status": "error",
            "data": "Publication order not found!"
        }, status=status.HTTP_404_NOT_FOUND) 
    serializer = BookSerializer(items, many=True)
    return Response({
        "status": "success",
        "data": serializer.data
    }, status=status.HTTP_200_OK)
# ==================================================================================================

# ============================== Edit information of a selected book ===============================
"""
    Schema for the possisble responses to a request for a book edit
"""
bookPutResponses = {
    "200": openapi.Response(
        description="Book updated successfully!",
        examples={
            "application/json": {
                "status": "success",
                "data": {
                    "id": "<int>",
                    "publication": "<int>",
                    "library": "<int>",
                    "condition": "<string>",
                    "section": "<int>",
                    "loaned": "<boolean>",
                    "reserved": "<boolean>"
                }
            }
        }
    ),
    "400": openapi.Response(
        description="Book update failed!",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    ),
    "401": openapi.Response(
        description="Book is in Library that is not managed by this Librarian!",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    ),
    "404": openapi.Response(
        description="Book not found!",
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
    tags=["Book"],
    method="PUT",
    operation_description="Update information of the book specified by Book ID",
    request_body=BookSerializer,
    responses=bookPutResponses
)
@api_view(['PUT'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian))])
def updateBook(request, id):
    """
        Function that allows user with an Administrator or Librarian role to list edit specified book.
        Expects user to be logged in and have required roles.
        Librarian can edit only Library that he is assigned to!
    """
    book = get_object_or_404(Book, id=id)
    if request.user.role == '3' and request.user.working_at is not book.library:
        return Response({
            "status": "error",
            "data": "You do not have permission to modify this book!"
        }, status=status.HTTP_401_UNAUTHORIZED) 
    serializer = BookSerializer(book, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": "success",
            "data": BookSerializer(book).data
        }, status=status.HTTP_200_OK)
    return Response({
        "status": "error",
        "data": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
# ==================================================================================================