from django.shortcuts import get_object_or_404;
from django.contrib.auth.signals import user_logged_in, user_logged_out
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_condition import And, Or
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from knox.models import AuthToken
from .permissions import IsAdministrator, IsDistributor, IsLibrarian, IsRegistredReader
from .serializers import AdminKeySerializer, LibrarySerializer, PublicationSerializer, UserSerializer, \
    UserNormalEditSerializer, UserAdminEditSerializer, \
    LoginSerializer, RegisterSerializer
from .models import Library, Account, Publication

# LibraryAPI ==========================================================================================================
## Get Library (either specified or all)
libraryGetResponses = {
    "200": openapi.Response(
        description="Retrieval of library information OK.",
        examples={
            "application/json": {
                "library": "<library_data>"
            }
        }
    )
}


@swagger_auto_schema(
    tags=["Library"],
    method="GET",
    operation_description="Allows users to get information about libraries",
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
@swagger_auto_schema(
    tags=["Library"],
    method="POST",
    operation_description="Allows user with Administration role to create new library",
    request_body=LibrarySerializer,
    responses=libraryGetResponses
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


## Associate Librarin with Library
@swagger_auto_schema(
    tags=["Library"],
    method="POST",
    operation_description="Allows user with role Administrator to assign Librarian to Library",
)
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, IsAdministrator)])
def associateLibrarianToLibrary(request, id, uid):
    library = Library.objects.get(id=id)
    librarian = Account.objects.get(id=uid)
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
        description="Retrieval of publication OK.",
        examples={
            "application/json": {
                "publication": "<publication_data>"
            }
        }
    )
}


@swagger_auto_schema(
    tags=["Publication"],
    method="GET",
    operation_description="Allows users to get information about Publications",
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
@swagger_auto_schema(
    tags=["Publication"],
    method="POST",
    operation_description="Allows users with Administrator, Librarian or Distributor role to create new Publication",
    request_body=PublicationSerializer,
    responses=publicationGetResponses  # TODO: Modify for POST method
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
@swagger_auto_schema(
    tags=["Publication"],
    method="PUT",
    operation_description="Allows users with Administrator, Librarian or Distributor role to update Publication",
    request_body=PublicationSerializer,
    responses=publicationGetResponses  # TODO: Modify for PUT method
)
@api_view(['PUT'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian, IsDistributor))])
def updatePublication(request, id):
    publication = Publication.objects.get(id=id)
    serializer = PublicationSerializer(publication, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": "success",
            "user": UserSerializer(publication).data
        }, status=status.HTTP_200_OK)
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST)


## Make Publication availiable at Library
@swagger_auto_schema(
    tags=["Publication"],
    method="POST",
    operation_description="Allows users with Administrator, Librarian or Distributor role to update Publication",
    responses=publicationGetResponses  # TODO: Modify for POST method
)
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian))])
def associatePublicationWithLibrary(request, id, lid):
    publication = Publication.objects.get(id=id)
    if publication is None:
        return Response({
            "status": "error",
            "data": "Failed to get publication.",
        }, status=status.HTTP_400_BAD_REQUEST)
    library = Library.objects.get(lid=lid)
    if library is None:
        return Response({
            "status": "error",
            "data": "Failed to get library.",
        }, status=status.HTTP_400_BAD_REQUEST)
    publication.availiable_at.add(library)
    publication.save()
    return Response({
        "status": "success",
    }, status=status.HTTP_200_OK)


# =====================================================================================================================

# OrderAPI ============================================================================================================
## Get Order (either specified by id or all)
OrderGetResponses = {
    "200": openapi.Response(
        description="Retrieval of PublicationOrder information OK.",
        examples={
            "application/json": {
                "PublicationOrder": "<PublicationOrder_data>"
            }
        }
    )
}


@swagger_auto_schema(
    tags=["Order"],
    method="GET",
    operation_description="Returns list of all orders in the system",
    responses=OrderGetResponses
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
    operation_description="Returns list of all orders in the system specified by library id",
    responses=OrderGetResponses
)
@api_view(['GET'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian, IsDistributor))])
def getOrderLibrarySpecified(request, id):
    item = get_object_or_404(PublicationOrder, library=id)
    serializer = PublicationOrderSerializer(item)
    return Response({
        "status": "success",
        "data": serializer.data
    }, status=status.HTTP_200_OK)


## Get Order specified by user id
@swagger_auto_schema(
    tags=["Order"],
    method="GET",
    operation_description="Returns list of all orders in the system specified by user id",
    responses=OrderGetResponses
)
@api_view(['GET'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian, IsDistributor))])
def getOrderUserSpecified(request, id):
    item = get_object_or_404(PublicationOrder, user=id)
    serializer = PublicationOrderSerializer(item)
    return Response({
        "status": "success",
        "data": serializer.data
    }, status=status.HTTP_200_OK)


## Get Order specified delivered and library
@swagger_auto_schema(
    tags=["Order"],
    method="GET",
    operation_description="Returns list of all orders in the system that were or were not delivered",
    responses=OrderGetResponses
)
@api_view(['GET'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian, IsDistributor))])
def getOrderDelivered(request, deliv, id):
    if id:
        items = get_object_or_404(Library, pk=id, delivered=deliv)
        serializer = PublicationOrderSerializer(items, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    items = get_object_or_404(PublicationOrder, delivered=deliv)
    serializer = PublicationOrderSerializer(items, many=True)
    return Response({
        "status": "success",
        "data": serializer.data
    }, status=status.HTTP_200_OK)


## Create new order
## TODO: NONFUNCTIONAL, no idea how to to this shit ##
@swagger_auto_schema(
    tags=["Order"],
    method="POST",
    operation_description="Allows Administrator or Librarian to create a new (world) order",
    request_body=,
    responses=OrderGetResponses  # TODO: Modify for POST method
)
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian))])
def createOrder(request):


## Update Order specified by PublicationOrder id
@swagger_auto_schema(
    tags=["Order"],
    method="PUT",
    operation_description="Set order specified by PublicationOrder ID as delivered",
    responses=OrderGetResponses  # TODO: Modify for PUT method
)
@api_view(['PUT'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsDistributor))])
def UpdateOrder(request, id):
    publicationOrder = Publication.objects.get(id=id)
    serializer = PublicationSerializer(publicationOrder, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": "success",
            "user": UserSerializer(publicationOrder).data
        }, status=status.HTTP_200_OK)
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST)


# =====================================================================================================================

# BookAPI =============================================================================================================
## Get Book (either specified by id or all)
OrderGetResponses = {
    "200": openapi.Response(
        description="Retrieval of Book information OK.",
        examples={
            "application/json": {
                "Book": "<Book_data>"
            }
        }
    )
}


@swagger_auto_schema(
    tags=["Book"],
    method="GET",
    operation_description="Returns list of all books in the system",
    responses=OrderGetResponses
)
@api_view(['GET'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian))])
def getOrder(request, id=None):
    if id:
        item = get_object_or_404(Book, pk=id)
        serializer = PublicationOrderSerializer(item)
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


# =====================================================================================================================

# UserAPI =============================================================================================================
## Get User
userGetResponses = {
    "200": openapi.Response(
        description="Retrieval of user information OK.",
        examples={
            "application/json": {
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
                "user": "<user_data>"
            }
        }
    ),
    "400": openapi.Response(
        description="Invalid data format."
    ),
    "401": openapi.Response(
        description="Unauthorized to get user details",
        examples={
            "application/json": {
                "detail": "Authentication credentials were not provided."
            }
        }
    ),
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
    user = Account.objects.get(email=request.user.email)
    serializer = UserNormalEditSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": "success",
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST)


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
    user = Account.objects.get(id=id)
    serializer = UserAdminEditSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": "success",
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST)


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
        description="Bad Request."
    ),
    "401": openapi.Response(
        description="Unauthorized to get user details",
        examples={
            "application/json": {
                "detail": "Authentication credentials were not provided."
            }
        }
    ),
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
    user = Account.objects.get(email=request.user.email)
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
    user = Account.objects.get(id=id)
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
@swagger_auto_schema(
    tags=["Administration"],
    method="POST",
    operation_description="Allows user to promote himself to Administrator if no other Administrator is defined yet",
    request_body=AdminKeySerializer,
    responses=publicationGetResponses  # TODO: Modify for POST method
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def makeAdministratorUsingKey(request):
    try:
        admin = Account.objects.get(role='4')
    except:
        pass
    else:
        return Response({
            "status": "error",
            "data": "Another Administrator already exists.",
        }, status=status.HTTP_400_BAD_REQUEST)
    user = Account.objects.get(email=request.user.email)
    if user is None:
        return Response({
            "status": "error",
            "data": "Failed to get user.",
        }, status=status.HTTP_400_BAD_REQUEST)
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
    responses=publicationGetResponses  # TODO: Modify for POST method
)
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, IsAdministrator)])
def makeAdministrator(request, id):
    user = Account.objects.get(id=id)
    if user is None:
        return Response({
            "status": "error",
            "data": "Failed to get user.",
        }, status=status.HTTP_400_BAD_REQUEST)
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
    responses=publicationGetResponses  # TODO: Modify for POST method
)
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, IsAdministrator)])
def makeLibrarian(request, id):
    user = Account.objects.get(id=id)
    if user is None:
        return Response({
            "status": "error",
            "data": "Failed to get user.",
        }, status=status.HTTP_400_BAD_REQUEST)
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
    responses=publicationGetResponses  # TODO: Modify for POST method
)
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, IsAdministrator)])
def makeDistributor(request, id):
    user = Account.objects.get(id=id)
    if user is None:
        return Response({
            "status": "error",
            "data": "Failed to get user.",
        }, status=status.HTTP_400_BAD_REQUEST)
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
    responses=publicationGetResponses  # TODO: Modify for POST method
)
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, IsAdministrator)])
def makeRegistredUser(request, id):
    user = Account.objects.get(id=id)
    if user is None:
        return Response({
            "status": "error",
            "data": "Failed to get user.",
        }, status=status.HTTP_400_BAD_REQUEST)
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
                "user": "<user_data>",
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
                "user": "<user_data>",
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