from django.shortcuts import get_object_or_404;
from django.contrib.auth.signals import user_logged_out
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_condition import And, Or
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from knox.models import AuthToken
from .permissions import IsAdministrator, IsDistributor, IsLibrarian, IsRegistredReader
from .serializers import AdminKeySerializer, BookLoanCreateSerializer, BookLoanSerializer, BookSerializer, \
    LibrarySerializer, \
    PublicationOrderCreateByAdmin, PublicationOrderCreateByLibrarian, PublicationOrderSerializer, \
    PublicationSerializer, UserSerializer, UserNormalEditSerializer, UserAdminEditSerializer, \
    LoginSerializer, RegisterSerializer, VotingSerializer
from .models import Book, BookLoan, BookOrder, Library, Account, Publication, PublicationOrder, Voting

# LibraryAPI ==========================================================================================================
## Get Library (either specified or all)
libraryGetResponses = {
    "200": openapi.Response(
        description="Library information successfully retrieved!",
        examples={
            "application/json": {
                "status": "success",
                "data": "<library_serialized_data>"
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


## Create Library
libraryPostResponses = {
    "200": openapi.Response(
        description="Library successfully created!",
        examples={
            "application/json": {
                "status": "success",
                "data": "<library_serialized_data>"
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


## Update Library
libraryPutResponses = {
    "200": openapi.Response(
        description="Library successfully updated!",
        examples={
            "application/json": {
                "status": "success",
                "data": "<library_serialized_data>"
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


## Associate Librarin with Library
libraryPostUserResponse = {
    "200": openapi.Response(
        description="Librarian successfully associated with library!",
        examples={
            "application/json": {
                "status": "success",
                "data": "<user_serialized_data>"
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


@swagger_auto_schema(
    tags=["Library"],
    method="POST",
    operation_description="Allows user with role Administrator to assign Librarian to a Library",
)
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, IsAdministrator)])
def associateLibrarianToLibrary(request, id, uid):
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


# =====================================================================================================================

# PublicationAPI ======================================================================================================
## Get Publication (either specified or all)
publicationGetResponses = {
    "200": openapi.Response(
        description="Publication data retrieved successfully!",
        examples={
            "application/json": {
                "status": "success",
                "data": "<publication_serialized_data>"
            }
        }
    ),
    "404": openapi.Response(
        description="Publication not found!",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    )
}


@swagger_auto_schema(
    tags=["Publication"],
    method="GET",
    operation_description="Allows users to list publications or display just selected one.",
    responses=publicationGetResponses,
    security=[]
)
@api_view(['GET'])
@permission_classes([AllowAny])
def getPublication(request, id=None):
    if id:
        item = get_object_or_404(Publication, pk=id)
        serializer = PublicationSerializer(item)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    items = Publication.objects.all()
    serializer = PublicationSerializer(items, many=True)
    return Response({
        "status": "success",
        "data": serializer.data
    }, status=status.HTTP_200_OK)


## Create Publication
publicationPostResponse = {
    "200": openapi.Response(
        description="Publication successfully created!",
        examples={
            "application/json": {
                "status": "success",
                "data": "<publication_serialized_data>"
            }
        }
    ),
    "400": openapi.Response(
        description="Publication creation failed!",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    )
}


@swagger_auto_schema(
    tags=["Publication"],
    method="POST",
    operation_description="Allows users with Administrator, Librarian or Distributor role to create new Publication",
    request_body=PublicationSerializer,
    responses=publicationPostResponse
)
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian, IsDistributor))])
def createPublication(request):
    serializer = PublicationSerializer(data=request.data)
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


## Update Publication
publicationPutResponse = {
    "200": openapi.Response(
        description="Publication successfully updated.",
        examples={
            "application/json": {
                "status": "success",
                "data": "<publication_serialized_data>"
            }
        }
    ),
    "400": openapi.Response(
        description="Publication update failed.",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    ),
    "404": openapi.Response(
        description="Publication not found!",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    )
}


@swagger_auto_schema(
    tags=["Publication"],
    method="PUT",
    operation_description="Allows users with Administrator, Librarian or Distributor role to update Publication",
    request_body=PublicationSerializer,
    responses=publicationPutResponse
)
@api_view(['PUT'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian, IsDistributor))])
def updatePublication(request, id):
    publication = get_object_or_404(Publication, id=id)
    serializer = PublicationSerializer(publication, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": "success",
            "data": PublicationSerializer(publication).data
        }, status=status.HTTP_200_OK)
    return Response({
            "status": "error",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


## Make Publication available at Library
publicationPostUserResponse = {
    "200": openapi.Response(
        description="Publication successfully associated with a library!",
        examples={
            "application/json": {
                "status": "success",
                "data": "<publication_serialized_data>"
            }
        }
    ),
    "400": openapi.Response(
        description="Association of publication with a library failed!",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    ),
    "404": openapi.Response(
        description="Publication or library not found!",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    )
}


@swagger_auto_schema(
    tags=["Publication"],
    method="POST",
    operation_description="Allows users with Administrator or Librarian role to associate Publication with a Library",
    responses=publicationPostUserResponse
)
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian))])
def associatePublicationWithLibrary(request, id, lid):
    publication = get_object_or_404(Publication, id=id)
    if publication is None:
        return Response({
            "status": "error",
            "data": "Failed to get publication.",
        }, status=status.HTTP_400_BAD_REQUEST)
    library = get_object_or_404(Library, id=lid)
    if library is None:
        return Response({
            "status": "error",
            "data": "Failed to get library.",
        }, status=status.HTTP_400_BAD_REQUEST)
    publication.available_at.add(library)
    publication.save()
    return Response({
        "status": "success",
        "data": PublicationSerializer(publication).data
    }, status=status.HTTP_200_OK)


# =====================================================================================================================

# OrderAPI ============================================================================================================
## Get Order (either specified by id or all)
orderGetResponses = {
    "200": openapi.Response(
        description="Publication order data retrieved successfully!",
        examples={
            "application/json": {
                "status": "success",
                "data": "<publicationorder_serialized_data>"
            }
        }
    ),
    "404": openapi.Response(
        description="Order not found!",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    )
}


@swagger_auto_schema(
    tags=["Order"],
    method="GET",
    operation_description="Returns list of all orders in the system or just information about the one specified by the id.",
    responses=orderGetResponses
)
@api_view(['GET'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian, IsDistributor))])
def getOrder(request, id=None):
    if id:
        item = get_object_or_404(PublicationOrder, pk=id)
        serializer = PublicationOrderSerializer(item)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    items = PublicationOrder.objects.all()
    serializer = PublicationOrderSerializer(items, many=True)
    return Response({
        "status": "success",
        "data": serializer.data
    }, status=status.HTTP_200_OK)


## Get Order specified by library id
@swagger_auto_schema(
    tags=["Order"],
    method="GET",
    operation_description="Returns list of all orders in the system for the library specified by library id",
    responses=orderGetResponses
)
@api_view(['GET'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian, IsDistributor))])
def getOrderLibrarySpecified(request, id):
    items = PublicationOrder.objects.filter(library=id)
    if not items:
        return Response({
            "status": "error",
            "data": "Publication order not found!"
        }, status=status.HTTP_404_NOT_FOUND) 
    serializer = PublicationOrderSerializer(items, many=True)
    return Response({
        "status": "success",
        "data": serializer.data
    }, status=status.HTTP_200_OK)


## Get Order specified by user id
@swagger_auto_schema(
    tags=["Order"],
    method="GET",
    operation_description="Returns list of all orders in the system specified by user id",
    responses=orderGetResponses
)
@api_view(['GET'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian, IsDistributor))])
def getOrderUserSpecified(request, id):
    items = PublicationOrder.objects.filter(user=id)
    if not items:
        return Response({
            "status": "error",
            "data": "Publication order not found!"
        }, status=status.HTTP_404_NOT_FOUND) 
    serializer = PublicationOrderSerializer(items, many=True)
    return Response({
        "status": "success",
        "data": serializer.data
    }, status=status.HTTP_200_OK)


## Get Order specified delivered and library
@swagger_auto_schema(
    tags=["Order"],
    method="GET",
    operation_description="Returns list of all orders in the system that were or were not delivered",
    responses=orderGetResponses
)
@api_view(['GET'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian, IsDistributor))])
def getOrderDelivered(request, delivered, id=None):
    if id:
        items = PublicationOrder.objects.filter(library=id).filter(delivered=delivered)
        if not items:
            return Response({
                "status": "error",
                "data": "Publication order not found!"
            }, status=status.HTTP_404_NOT_FOUND) 
        serializer = PublicationOrderSerializer(items, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    items = PublicationOrder.objects.filter(delivered=delivered)
    if not items:
        return Response({
            "status": "error",
            "data": "Publication order not found!"
        }, status=status.HTTP_404_NOT_FOUND) 
    serializer = PublicationOrderSerializer(items, many=True)
    return Response({
        "status": "success",
        "data": serializer.data
    }, status=status.HTTP_200_OK)


## Create new order
orderPostResponses = {
    "200": openapi.Response(
        description="Publication order successfully created!",
        examples={
            "application/json": {
                "status": "success"
            }
        }
    ),
    "400": openapi.Response(
        description="Publication order creation failed!",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    )
}


@swagger_auto_schema(
    tags=["Order"],
    method="POST",
    operation_description="Allows Administrator or Librarian to create a new publication order",
    request_body=PublicationOrderCreateByLibrarian,
    responses=orderPostResponses
)
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian))])
def createOrder(request):
    if request.user.role == '3':
        if not request.user.working_at:
            return Response({
                "status": "error",
                "data": "Librarian is not assigned to any library!"
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer = PublicationOrderCreateByLibrarian(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user, library=request.user.working_at)
            return Response({
                "status": "success"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": "error",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    else:
        serializer = PublicationOrderCreateByAdmin(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response({
                "status": "success"
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": "error",
                "data": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


## Mark order as delivered
orderPostDeliverResponses = {
    "200": openapi.Response(
        description="Publication order successfully delivered!",
        examples={
            "application/json": {
                "status": "success",
            }
        }
    ),
    "400": openapi.Response(
        description="Publication order already delivered!",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    ),
    "404": openapi.Response(
        description="Publication order not found!",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    )
}


@swagger_auto_schema(
    tags=["Order"],
    method="POST",
    operation_description="Set order specified by PublicationOrder ID as delivered",
    responses=orderPostDeliverResponses
)
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsDistributor))])
def deliverOrder(request, id):
    publicationOrder = get_object_or_404(PublicationOrder, id=id)
    if publicationOrder.delivered:
        return Response({
            "status": "failure",
            "data": "Specified order is already delivered!"
        }, status=status.HTTP_400_BAD_REQUEST)
    publicationOrder.delivered = True
    publicationOrder.save()
    book_order = get_object_or_404(BookOrder, publication_order=id)
    for i in range(book_order.number_of_books):
        book = Book()
        book.publication = publicationOrder.publication
        book.library = publicationOrder.library
        book.section = 1
        book.save()
    return Response({
        "status": "success"
    }, status=status.HTTP_200_OK)


# =====================================================================================================================

# BookAPI =============================================================================================================
## Get Book (either specified by id or all)
bookGetResponses = {
    "200": openapi.Response(
        description="Book information retrieved successfully!",
        examples={
            "application/json": {
                "status": "success",
                "data": "<book_serialized_data>"
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


## Get Books in a specific library
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


## Update book information
bookPutResponses = {
    "200": openapi.Response(
        description="Book updated successfully!",
        examples={
            "application/json": {
                "status": "success",
                "data": "<book_serialized_data>"
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
# =====================================================================================================================

# BookLoanAPI =========================================================================================================
## Get BookLoan (either specified by id or all)
loanGetResponses = {
    "200": openapi.Response(
        description="Retrieval of BookLoan information OK.",
        examples={
            "application/json": {
            "status": "success",
            "data": "<bookloan_serialized_data>"
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


@swagger_auto_schema(
    tags=["Book Loan"],
    method="GET",
    operation_description="Returns list of all book loans in the system or just one specified by an id",
    responses=loanGetResponses
)
@api_view(['GET'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian))])
def getLoan(request, id=None):
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

## Get BookLoan from the library specified by id
@swagger_auto_schema(
    tags=["Book Loan"],
    method="GET",
    operation_description="Returns list of all book loans in the system in the library specified by library id",
    responses=loanGetResponses
)
@api_view(['GET'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian))])
def getLoanInLibrary(request, id):
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

## Get BookLoans of the user specified by id
@swagger_auto_schema(
    tags=["Book Loan"],
    method="GET",
    operation_description="Returns list of all book loans in the system that user specified by user id made",
    responses=loanGetResponses
)
@api_view(['GET'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian))])
def getLoanUserByID(request, id):
    items = get_object_or_404(BookLoan, user=id)
    serializer = BookLoanSerializer(items)
    return Response({
        "status": "success",
        "data": serializer.data
    }, status=status.HTTP_200_OK)

## Get BookLoans of the user specified by id
@swagger_auto_schema(
    tags=["Book Loan"],
    method="GET",
    operation_description="Get list of loans that logged in user made",
    responses=loanGetResponses
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getLoanUser(request):
    items = get_object_or_404(BookLoan, user=request.user)
    serializer = BookLoanSerializer(items)
    return Response({
        "status": "success",
        "data": serializer.data
    }, status=status.HTTP_200_OK)

## Create a new BookLoan
bookLoanPostResponses = {
    "200": openapi.Response(
        description="Creation of book loan successfull!",
        examples={
            "application/json": {
            "status": "success",
            "data": "<bookloan_serialized_data>"
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
    serializer = BookLoanCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(creator=request.user)
        return Response({
           "status": "success"
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "status": "error",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

## Confirm BookLoan
@swagger_auto_schema(
    tags=["Book Loan"],
    method="POST",
    operation_description="Confirm loan",
    responses=bookLoanPostResponses
)
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian))])
def confirmLoan(request, id):
    loan = get_object_or_404(BookLoan, id=id)
    loan.loans = request.user
    loan.save()
    for book in loan.books.all():
        book.loaned = True
        book.save()
    return Response({
        "status": "success"
    }, status=status.HTTP_200_OK)

## Create a new BookLoan as an UnregisteredUser
#@swagger_auto_schema(
#   tags=["Book Loan"],
#   method="POST",
#   operation_description="An unregistered user creates new book loan",
#   responses= # TODO: response
#)
#@api_view(['POST'])
#def createLoanUnregistered(request):
#
# loanBook
# receiveBook
#
## Add fine to a BookLoan
#@swagger_auto_schema(
#    tags=["Book Loan"],
#    method="PUT",
#    operation_description="Adds or updates a fine for BookLoan specified by id",
#    responses=loanGetResponses # TODO: update for put request
#)
#@api_view(['PUT'])
#@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian))])
#def updateLoan(request, id):
#    bookloan = BookLoan.objects.get(id=id)
#    serializer = BookLoanSerializer(bookloan, data=request.data)
#    if serializer.is_valid():
#        serializer.save()
#        return Response({
#            "status": "success",
#            "BookLoan": BookLoanSerializer(bookloan).data
#            }, status=status.HTTP_200_OK)
#    return Response(
#        serializer.errors,
#        status=status.HTTP_400_BAD_REQUEST)
# =====================================================================================================================

# VotingAPI ===========================================================================================================
## Get Voting (either specified by id or all)
votingGetResponses = {
    "200": openapi.Response(
        description="Retrieval of voting information OK.",
        examples={
            "application/json": {
            "status": "success",
            "data": "<voting_serialized_data>"
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
        description="Voting not found!",
        examples={
            "application/json": {
                "status": "error",
                "data": "<error_details>"
            }
        }
    )
}


@swagger_auto_schema(
    tags=["Voting"],
    method="GET",
    operation_description="Returns list of all voting in the system or just one specified by an id",
    responses=votingGetResponses
)
@api_view(['GET'])
@permission_classes([AllowAny])
def getVoting(request, id=None):
    if id:
        item = get_object_or_404(Voting, pk=id)
        serializer = VotingSerializer(item)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    items = Voting.objects.all()
    serializer = VotingSerializer(items, many=True)
    return Response({
        "status": "success",
        "data": serializer.data
    }, status=status.HTTP_200_OK)

## Get voting in a specificied by library id
@swagger_auto_schema(
    tags=["Voting"],
    method="GET",
    operation_description="Returns list of all voting in the system for the library specified by library id",
    responses=votingGetResponses
)
@api_view(['GET'])
@permission_classes([AllowAny])
def getLibraryVoting(request, id):
    items = Voting.objects.filter(library=id)
    if not items:
        return Response({
            "status": "error",
            "data": "No voting found!"
        }, status=status.HTTP_404_NOT_FOUND)
    serializer = VotingSerializer(items, many=True)
    return Response({
        "status": "success",
        "data": serializer.data
    }, status=status.HTTP_200_OK)

# =====================================================================================================================

# UserAPI =============================================================================================================
## Get User
userGetResponses = {
    "200": openapi.Response(
        description="Retrieval of user information OK.",
        examples={
            "application/json": {
                "status": "success",
                "user": "<user_data>"
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


@swagger_auto_schema(
    tags=["User"],
    method="GET",
    operation_description="Allows user to get his own information",
    responses=userGetResponses
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUser(request):
    return Response({
        "status": "success",
        "user": UserSerializer(request.user).data
    }, status=status.HTTP_200_OK)


## Get Specified User
@swagger_auto_schema(
    tags=["User"],
    method="GET",
    operation_description="Allows user with role of Administrator or Librarian to get information about specified user",
    responses=userGetResponses
)
@api_view(['GET'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian))])
def getUserByID(request, id):
    user = get_object_or_404(Account, pk=id)
    return Response({
        "status": "success",
        "user": UserSerializer(user).data
    }, status=status.HTTP_200_OK)


## Edit User
userPutResponses = {
    "200": openapi.Response(
        description="User updated!",
        examples={
            "application/json": {
                "status": "success",
                "user": "<user_data>"
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


## Edit Specified User
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


## Delete User
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


@swagger_auto_schema(
    tags=["User"],
    method="DELETE",
    operation_description="Deletes user",
    responses=userDeleteResponses
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteUser(request):
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


## Delete Specified User
@swagger_auto_schema(
    tags=["User"],
    method="DELETE",
    operation_description="Allows user with Administrator permission to delete specified user",
    responses=userDeleteResponses
)
@api_view(['DELETE'])
@permission_classes([And(IsAuthenticated, IsAdministrator)])
def deleteUserByID(request, id):
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


## List All Users
@swagger_auto_schema(
    tags=["User"],
    method="GET",
    operation_description="Lists all users from the system",
    responses=userGetResponses
)
@api_view(['GET'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian))])
def getAllUsers(request):
    users = Account.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response({
        "status": "success",
        "data": serializer.data
    }, status=status.HTTP_200_OK)


# =====================================================================================================================

# AdminAPI ============================================================================================================
## Set user's role to Administrator
adminPostResponses = {
    "200": openapi.Response(
        description="User promoted!",
        examples={
            "application/json": {
                "status": "success",
                "data": "<user_serialized_data>"
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


@swagger_auto_schema(
    tags=["Administration"],
    method="POST",
    operation_description="Allows user to promote himself to Administrator if no other Administrator is defined yet",
    request_body=AdminKeySerializer,
    responses=adminPostResponses
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def makeAdministratorUsingKey(request):
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


## Set user's role to Administrator
@swagger_auto_schema(
    tags=["Administration"],
    method="POST",
    operation_description="Allows users with Administrator role to change selected user's role to Administrator",
    responses=adminPostResponses
)
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, IsAdministrator)])
def makeAdministrator(request, id):
    user = get_object_or_404(Account, id=id)
    user.role = '4'
    user.save()
    return Response({
        "status": "success",
        "data": UserSerializer(user).data
    }, status=status.HTTP_200_OK)


## Set user's role to Librarian
@swagger_auto_schema(
    tags=["Administration"],
    method="POST",
    operation_description="Allows users with Administrator role to change selected user's role to Librarian",
    responses=adminPostResponses
)
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, IsAdministrator)])
def makeLibrarian(request, id):
    user = get_object_or_404(Account, id=id)
    user.role = '3'
    user.save()
    return Response({
        "status": "success",
        "data": UserSerializer(user).data
    }, status=status.HTTP_200_OK)


## Set user's role to Distributor
@swagger_auto_schema(
    tags=["Administration"],
    method="POST",
    operation_description="Allows users with Administrator role to change selected user's role to Distributor",
    responses=adminPostResponses
)
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, IsAdministrator)])
def makeDistributor(request, id):
    user = get_object_or_404(Account, id=id)
    user.role = '2'
    user.save()
    return Response({
        "status": "success",
        "data": UserSerializer(user).data
    }, status=status.HTTP_200_OK)


## Set user's role to Registred User
@swagger_auto_schema(
    tags=["Administration"],
    method="POST",
    operation_description="Allows users with Administrator role to change selected user's role to Registred User",
    responses=adminPostResponses
)
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, IsAdministrator)])
def makeRegistredUser(request, id):
    user = get_object_or_404(Account, id=id)
    user.role = '1'
    user.save()
    return Response({
        "status": "success",
        "data": UserSerializer(user).data
    }, status=status.HTTP_200_OK)


# =====================================================================================================================

# AuthenticationAPI ===================================================================================================
## Register new account
userRegisterResponses = {
    "201": openapi.Response(
        description="Registration Successful.",
        examples={
            "application/json": {
                "status": "success",
                "user": "<user_serialized_data>",
                "token": "<user_token>"
            }
        }
    ),
    "400": openapi.Response(
        description="Registration Failed",
        examples={
            "application/json": {
                "username": "account with this username already exists."
            }
        }
    ),
}


@swagger_auto_schema(
    tags=["Authorization"],
    method="POST",
    operation_description="Allows unregistred visitor to create account.",
    request_body=RegisterSerializer,
    responses=userRegisterResponses,
    security=[]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def UserRegistration(request, *args, **kwargs):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    return Response({
        "status": "success",
        "user": UserSerializer(user).data,
        "token": AuthToken.objects.create(user)[1]
    }, status=status.HTTP_201_CREATED)


## Login existing user
userLoginResponses = {
    "200": openapi.Response(
        description="Login Success.",
        examples={
            "application/json": {
                "status": "success",
                "user": "<user_serialized_data>",
                "token": "<user_token>"
            }
        }
    ),
    "400": openapi.Response(
        description="Login Failed",
        examples={
            "application/json": {
                "non_field_errors": "Invalid details."
            }
        }
    ),
}


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
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data

    return Response({
        "status": "success",
        "user": UserSerializer(user).data,
        "token": AuthToken.objects.create(user)[1]
    }, status=status.HTTP_200_OK)
# =====================================================================================================================