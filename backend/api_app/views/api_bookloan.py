from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_condition import And, Or
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api_app.models import BookLoan, Library, WaitingList
from api_app.permissions import IsAdministrator, IsLibrarian
from api_app.serializers import BookLoanCreateSerializer, BookLoanSerializer, WaitingListSerializer

"""
    Schema for the possisble responses to a request for an bookloan information
"""
loanGetResponses = {
    "200": openapi.Response(
        description="Retrieval of BookLoan information OK.",
        examples={
            "application/json": {
            "status": "success",
            "data": [
                {
                    "id": "<int>",
                    "user": "<int>",
                    "loans": "<int>",
                    "receives": "<null>",
                    "date_from": "<date_time>",
                    "date_to": "<date_time>",
                    "extension_to": "<null>",
                    "fine": "<int>",
                    "books": [
                        "<book_ids>"
                    ]
                }
            ]
            }
        }
    ),
    "401": openapi.Response(
        description="Unauthorized!",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    ),
    "404": openapi.Response(
        description="Book loan not found!",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    )
}
# =================== List information about all bookloans or just specified one ===================
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Book Loan"],
    method="GET",
    operation_description="Returns list of all book loans in the system or just one specified by an id",
    responses=loanGetResponses
)
@api_view(['GET'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian))])
def getLoan(request, id=None):
    """
        Function that allows user with Administrator or Librarian role to list all bookloans or just specified one.
        This function expects user to be logged in.
    """
    if id:
        item = get_object_or_404(BookLoan, pk=id)
        serializer = BookLoanSerializer(item)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    items = BookLoan.objects.all()
    serializer = BookLoanSerializer(items, many=True)
    return Response({
        "status": "success",
        "data": serializer.data
    }, status=status.HTTP_200_OK)
# ==================================================================================================

# ================================== List bookloans by a library ===================================
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Book Loan"],
    method="GET",
    operation_description="Returns list of all book loans in the system in the library specified by library id",
    responses=loanGetResponses
)
@api_view(['GET'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian))])
def getLoanInLibrary(request, id):
    """
        Function that allows user with Administrator or Librarian role to list bookloans in library.
        This function expects user to be logged in.
    """
    if request.user.role == '3' and request.user.working_at != get_object_or_404(Library, id=id):
        return Response({
            "status": "error",
            "data": "Librarian doesn't have access to this Library!"
        }, status=status.HTTP_401_UNAUTHORIZED) 
    items = BookLoan.objects.filter(library=id)
    if not items:
        return Response({
            "status": "error",
            "data": "Book loan for library not found!"
        }, status=status.HTTP_404_NOT_FOUND) 
    serializer = BookLoanSerializer(items, many=True)
    return Response({
        "status": "success",
        "data": serializer.data
    }, status=status.HTTP_200_OK)
# ==================================================================================================

# =================================== List bookloans by a user =====================================
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Book Loan"],
    method="GET",
    operation_description="Returns list of all book loans in the system that user specified by user id made",
    responses=loanGetResponses
)
@api_view(['GET'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian))])
def getLoanUserByID(request, id):
    """
        Function that allows user with Administrator or Librarian role to list bookloans made by user.
        This function expects user to be logged in.
    """
    items = BookLoan.objects.filter(user=id)
    if not items:
        return Response({
            "status": "error",
            "data": "Book loan for a user not found!"
        }, status=status.HTTP_404_NOT_FOUND) 
    serializer = BookLoanSerializer(items, many=True)
    return Response({
        "status": "success",
        "data": serializer.data
    }, status=status.HTTP_200_OK)
# ==================================================================================================

# ============================= List bookloans by a logged in user =================================
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Book Loan"],
    method="GET",
    operation_description="Get list of loans that logged in user made",
    responses=loanGetResponses
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getLoanUser(request):
    """
        Function that allows user to list bookloans he made.
        This function expects user to be logged in.
    """
    items = BookLoan.objects.filter(user=request.user)
    if not items:
        return Response({
            "status": "error",
            "data": "Book loan for a user not found!"
        }, status=status.HTTP_404_NOT_FOUND) 
    serializer = BookLoanSerializer(items, many=True)
    return Response({
        "status": "success",
        "data": serializer.data
    }, status=status.HTTP_200_OK)
# ==================================================================================================

"""
    Schema for the possisble responses to a request for an bookloan create or edit
"""
bookLoanPostResponses = {
    "200": openapi.Response(
        description="Creation or update of a book loan successfull!",
        examples={
            "application/json": {
                "status": "success or waiting"
            }
        }
    ),
    "401": openapi.Response(
        description="Unauthorized!",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    ),
    "404": openapi.Response(
        description="Something not found!",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    )
}
# ===================================== Create a new bookloan ======================================
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Book Loan"],
    method="POST",
    operation_description="A registered user creates new book loan",
    request_body=BookLoanCreateSerializer,
    responses=bookLoanPostResponses
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createLoan(request):
    """
        Function that allows user to create bew bookloans.
        This function expects user to be logged in.
    """
    serializer = BookLoanCreateSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save(creator=request.user)
        except ValidationError:
            return Response({
                "status": "waiting"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": "success"
            }, status=status.HTTP_200_OK)
    else:
        return Response({
            "status": "error",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
# ==================================================================================================

# ====================================== Confirm a bookloan ========================================
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Book Loan"],
    method="POST",
    operation_description="Confirm loan",
    responses=bookLoanPostResponses
)
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian))])
def confirmLoan(request, id):
    """
        Function that allows user with Administrator or Librarian role to confirm a bookloan.
        This function expects user to be logged in.
    """
    loan = get_object_or_404(BookLoan, id=id)
    if request.user.role == '3' and request.user.working_at != loan.library:
        return Response({
            "status": "error",
            "data": "Librarian doesn't have access to this Library!"
        }, status=status.HTTP_401_UNAUTHORIZED)
    if loan.loans is not None:
        return Response({
            "status": "error",
            "data": "Loan already confirmed!"
        }, status=status.HTTP_400_BAD_REQUEST)
    for book in loan.books.all():
        if book.loaned:
            return Response({
                "status": "error",
                "data": "Some of the books are already loaned to someone else!"
            }, status=status.HTTP_400_BAD_REQUEST)
    loan.loans = request.user
    loan.save()
    for book in loan.books.all():
        book.loaned = True
        book.save()
    return Response({
        "status": "success"
    }, status=status.HTTP_200_OK)
# ==================================================================================================

# ====================================== Receive a bookloan ========================================
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Book Loan"],
    method="POST",
    operation_description="Receive loaned books",
    responses=bookLoanPostResponses
)
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian))])
def receiveLoan(request, id):
    """
        Function that allows user with Administrator or Librarian role to receive a bookloan.
        Receive means returning loan back to a library.
        This function expects user to be logged in.
    """
    loan = get_object_or_404(BookLoan, id=id)
    if request.user.role == '3' and request.user.working_at != loan.library:
        return Response({
            "status": "error",
            "data": "Librarian doesn't have access to this Library!"
        }, status=status.HTTP_401_UNAUTHORIZED)
    if loan.receives is not None:
        return Response({
            "status": "error",
            "data": "Loan already returned!"
        }, status=status.HTTP_400_BAD_REQUEST)
    loan.receives = request.user
    loan.save()
    for book in loan.books.all():
        book.loaned = False
        book.reserved = False
        book.save()
    # TODO: Check WaitingList and create new bookloans if availiable
    return Response({
        "status": "success"
    }, status=status.HTTP_200_OK)
# ==================================================================================================

# ================================== Add a fine to a bookloan ======================================
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Book Loan"],
    method="PUT",
    operation_description="Adds or updates a fine for BookLoan specified by id",
    responses=bookLoanPostResponses
)
@api_view(['PUT'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian))])
def updateLoan(request, id, fine):
    """
        Function that allows user with Administrator or Librarian role to add a fine to a bookloan.
        This function expects user to be logged in.
    """
    loan = get_object_or_404(BookLoan, id=id)
    if request.user.role == '3' and request.user.working_at != loan.library:
        return Response({
            "status": "error",
            "data": "Librarian doesn't have access to this Library!"
        }, status=status.HTTP_401_UNAUTHORIZED)
    loan.fine = loan.fine + fine
    loan.save()
    return Response({
        "status": "success"
    }, status=status.HTTP_200_OK)
# ==================================================================================================