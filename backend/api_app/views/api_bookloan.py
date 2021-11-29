import datetime
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_condition import And, Or
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api_app.models import Account, Book, BookLoan, Library, WaitingList
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
    waits = WaitingList.objects.all()
    serializer = BookLoanSerializer(items, many=True)
    serializer_w = WaitingListSerializer(waits, many=True)
    return Response({
        "status": "success",
        "data": serializer.data,
        "additional": serializer_w.data
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
    waits = WaitingList.objects.filter(library=id)
    if not items:
        return Response({
            "status": "error",
            "data": "Book loan for library not found!"
        }, status=status.HTTP_404_NOT_FOUND) 
    serializer = BookLoanSerializer(items, many=True)
    serializer_w = WaitingListSerializer(waits, many=True)
    return Response({
        "status": "success",
        "data": serializer.data,
        "additional": serializer_w.data
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
    waits = WaitingList.objects.filter(user=id)
    if not items and not waits:
        return Response({
            "status": "error",
            "data": "Book loan for a user not found!"
        }, status=status.HTTP_404_NOT_FOUND) 
    serializer = BookLoanSerializer(items, many=True)
    serializer_w = WaitingListSerializer(waits, many=True)
    return Response({
        "status": "success",
        "data": serializer.data,
        "additional": serializer_w.data
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
    waits = WaitingList.objects.filter(user=request.user)
    if not items and not waits:
        return Response({
            "status": "error",
            "data": "Book loan for a user not found!"
        }, status=status.HTTP_404_NOT_FOUND) 
    serializer = BookLoanSerializer(items, many=True)
    serializer_w = WaitingListSerializer(waits, many=True)
    return Response({
        "status": "success",
        "data": serializer.data,
        "additional": serializer_w.data
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
def createLoan(request, uid=None):
    """
        Function that allows user to create bew bookloans.
        This function expects user to be logged in.
    """
    serializer = BookLoanCreateSerializer(data=request.data)
    if serializer.is_valid():
        try:
            if uid:
                serializer.save(creator=get_object_or_404(Account, id=uid))
            else:
                serializer.save(creator=request.user)
        except ValidationError:
            return Response({
                "status": "waiting"
            }, status=status.HTTP_200_OK)
        except ValueError:  
            return Response({
                "status": "error",
                "data": "Invalid data! Probably books from different libraries!"
            }, status=status.HTTP_400_BAD_REQUEST)
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
def checkListIfAvailable(list):
    for id in list:
        book = Book.objects.get(id=id)
        if not book:
            return False
        if book.reserved or book.loaned:
            return False
    return True

def checkListIfValid(list):
    library = None
    for id in list:
        book = Book.objects.get(id=id)
        if not book:
            return False
        if library is None:
            library = book.library
        if library.id != book.library.id:
            return False
    return True

def checkWaitingList():
    found_possible = False
    waiting_list = WaitingList.objects.all().order_by('date_created')
    for reservation in waiting_list:
        if checkListIfAvailable(reservation.books) and checkListIfValid(reservation.books):
            book_loan = BookLoan()
            book_loan.user = reservation.user
            book_loan.library = reservation.library
            book_loan.date_from = reservation.date_from
            book_loan.date_to = reservation.date_to
            book_loan.save()
            for id in reservation.books:
                book = get_object_or_404(Book, id=id)
                book.reserved = True
                book_loan.books.add(book)
                book.save()
            book_loan.save()
            reservation.delete()
            found_possible = True
    return found_possible

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
    if checkWaitingList():
        return Response({
            "status": "success",
            "updated": "waiting_list",
            "details": "Found new possible book loand and created it!"
        }, status=status.HTTP_200_OK)
    else:
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

# ======================================= Extend bookloan ==========================================
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Book Loan"],
    method="POST",
    operation_description="Extend loan by X days",
    responses=bookLoanPostResponses
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def extendLoan(request, id, days):
    """
        Function that allows user with Administrator, Librarian role or owner of loan to extend it by X days.
        This function expects user to be logged in.
    """
    loan = get_object_or_404(BookLoan, id=id)
    if days > 30:
        return Response({
            "status": "error",
            "data": "Loan can be extended by max of 30 days!"
        }, status=status.HTTP_400_BAD_REQUEST)
    if loan.extension_to and (request.user.role != '4' or request.user.role != '3'):
        return Response({
            "status": "error",
            "data": "Loan can be extended just once!"
        }, status=status.HTTP_400_BAD_REQUEST)
    if request.user.role == '3' and request.user.working_at != loan.library:
        return Response({
            "status": "error",
            "data": "Librarian doesn't have access to this Library!"
        }, status=status.HTTP_401_UNAUTHORIZED)
    if (request.user.role == '1' or request.user.role == '2') and loan.user != request.user:
        return Response({
            "status": "error",
            "data": "User is not owner of this book loan!"
        }, status=status.HTTP_401_UNAUTHORIZED)
    if loan.extension_to:
        original_date = loan.extension_to
    else:
        original_date = loan.date_to
    loan.extension_to = original_date + datetime.timedelta(days=days)
    loan.save()
    return Response({
        "status": "success"
    }, status=status.HTTP_200_OK)
# ==================================================================================================