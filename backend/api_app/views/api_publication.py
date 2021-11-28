from django.shortcuts import get_object_or_404
from rest_condition import And, Or
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api_app.models import Book, Library, Publication, Voting
from api_app.permissions import IsAdministrator, IsDistributor, IsLibrarian
from api_app.serializers import BookSerializer, PublicationSerializer

# ================= List information about all publications or just selected one ===================
"""
    Schema for the possisble responses to a request for a publication information
"""
publicationGetResponses = {
    "200": openapi.Response(
        description="Publication data retrieved successfully!",
        examples={
            "application/json": {
                "status": "success",
                "data": [
                    {
                    "id": "<int>",
                    "name": "<string>",
                    "series": "<string>",
                    "synopsis": "<string>",
                    "authors": "<string>",
                    "language": "<string>",
                    "ISBN": "<string>",
                    "date_of_publication": "<date_time>",
                    "publisher": "<string>",
                    "genre": "<string>",
                    "pages": "<int>",
                    "tags": "<string>",
                    "rating": "<float>",
                    "available_at": [
                        "<int>"
                    ],
                    "rated_sum": "<int>",
                    "rated_times": "<int>"
                    }
                ]
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
"""
    Settings for Swagger OpenAPI documentation
"""
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
    """
        Function that allows users to list all publications or just selected one.
    """
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
# ==================================================================================================

# ========================== Check if publication is available in library ==========================
"""
    Schema for the possisble responses to a request for a publication check
"""
publicationCheckResponses = {
    "200": openapi.Response(
        description="Publication data retrieved successfully!",
        examples={
            "application/json": {
                "status": "available",
                "available": "<int>",
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
            },
            "application/json": {
                "status": "owned",
                "owned": "<int>",
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
        description="Publication not found!",
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
    tags=["Publication"],
    method="GET",
    operation_description="Allows users check if publication is available at specified library",
    responses=publicationCheckResponses,
    security=[]
)
@api_view(['GET'])
@permission_classes([AllowAny])
def getPublicationInLibrary(request, id, lid):
    """
        Function that allows users to check if publication is available at library.
    """
    publication = get_object_or_404(Publication, id=id)
    library = get_object_or_404(Library, id=lid)
    if library in publication.available_at.all():
        all_books = Book.objects.filter(publication=id).filter(library=lid)
        total = all_books.count()
        availiable_books = Book.objects.filter(publication=id).filter(library=lid).filter(loaned=False)
        availiable = availiable_books.count()
        serializer_all = BookSerializer(all_books, many=True)
        serializer_ava = BookSerializer(availiable_books, many=True)
        if availiable > 0:
            return Response({
                "status": "available",
                "available": availiable,
                "data": serializer_ava.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": "owned",
                "owned": total,
                "data": serializer_all.data
            }, status=status.HTTP_200_OK)
    return Response({
        "status": "not_available"
    }, status=status.HTTP_404_NOT_FOUND)
# ==================================================================================================

# ============================= List publications in selected library ==============================
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Publication"],
    method="GET",
    operation_description="Allows users what publications are availiable at specified library",
    responses=publicationGetResponses,
    security=[]
)
@api_view(['GET'])
@permission_classes([AllowAny])
def getPublicationsInLibrary(request, lid):
    """
        Function that allows users to check publications in selected library
    """
    items = Publication.objects.filter(available_at=lid)
    if items is None:
        return Response({
            "status": "error"
        }, status=status.HTTP_404_NOT_FOUND)
    serializer = PublicationSerializer(items, many=True)
    return Response({
        "status": "success",
        "data": serializer.data
    }, status=status.HTTP_200_OK)
# ==================================================================================================   

# ==================================== Create new publication ======================================
"""
    Schema for the possisble responses to a request for a publication create
"""
publicationPostResponse = {
    "200": openapi.Response(
        description="Publication successfully created!",
        examples={
            "application/json": {
                "status": "success",
                "data": {
                    "id": "<int>",
                    "name": "<string>",
                    "series": "<string>",
                    "synopsis": "<string>",
                    "authors": "<string>",
                    "language": "<string>",
                    "ISBN": "<string>",
                    "date_of_publication": "<date_time>",
                    "publisher": "<string>",
                    "genre": "<string>",
                    "pages": "<int>",
                    "tags": "<string>",
                    "rating": "<float>",
                    "available_at": [
                        "<int>"
                    ],
                    "rated_sum": "<int>",
                    "rated_times": "<int>"
                }
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
"""
    Settings for Swagger OpenAPI documentation
"""
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
    """
        Function that allows users with selected role to create a new publications.
    """
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
# ==================================================================================================

# ================================== Edit existing publication =====================================
"""
    Schema for the possisble responses to a request for a publication edit
"""
publicationPutResponse = {
    "200": openapi.Response(
        description="Publication successfully updated.",
        examples={
            "application/json": {
                "status": "success",
                "data": {
                    "id": "<int>",
                    "name": "<string>",
                    "series": "<string>",
                    "synopsis": "<string>",
                    "authors": "<string>",
                    "language": "<string>",
                    "ISBN": "<string>",
                    "date_of_publication": "<date_time>",
                    "publisher": "<string>",
                    "genre": "<string>",
                    "pages": "<int>",
                    "tags": "<string>",
                    "rating": "<float>",
                    "available_at": [
                        "<int>"
                    ],
                    "rated_sum": "<int>",
                    "rated_times": "<int>"
                }
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
"""
    Settings for Swagger OpenAPI documentation
"""
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
    """
        Function that allows users with selected roles to edit existing publications.
    """
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
# ==================================================================================================

# ================================ Add Publication to a Library ====================================
"""
    Schema for the possisble responses to a request for a publication edit
"""
publicationPostUserResponse = {
    "200": openapi.Response(
        description="Publication successfully associated with a library!",
        examples={
            "application/json": {
                "status": "success",
                "data": {
                    "id": "<int>",
                    "name": "<string>",
                    "series": "<string>",
                    "synopsis": "<string>",
                    "authors": "<string>",
                    "language": "<string>",
                    "ISBN": "<string>",
                    "date_of_publication": "<date_time>",
                    "publisher": "<string>",
                    "genre": "<string>",
                    "pages": "<int>",
                    "tags": "<string>",
                    "rating": "<float>",
                    "available_at": [
                        "<int>"
                    ],
                    "rated_sum": "<int>",
                    "rated_times": "<int>"
                }
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
    "400": openapi.Response(
        description="Unauthorized!",
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
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Publication"],
    method="POST",
    operation_description="Allows users with Administrator or Librarian role to associate Publication with a Library",
    responses=publicationPostUserResponse
)
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian))])
def associatePublicationWithLibrary(request, id, lid):
    """
        Function that allows users with selected roles to add a publication to a library
    """
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
    if request.user.role == '3' and request.user.working_at is not library:
        return Response({
            "status": "error",
            "data": "Librarian doesn't have access to this Library.",
        }, status=status.HTTP_401_UNAUTHORIZED)
    publication.available_at.add(library)
    publication.save()
    # Create voting when publication is added to a library
    new_voting = Voting()
    new_voting.library = library
    new_voting.publication = publication
    new_voting.votes = 0
    new_voting.save()
    return Response({
        "status": "success",
        "data": PublicationSerializer(publication).data
    }, status=status.HTTP_200_OK)
# ==================================================================================================

# =================================== Add a rating to a publication ================================
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Publication"],
    method="POST",
    operation_description="Allows users to rate publication",
    responses=publicationPostUserResponse
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ratePublication(request, id, rate):
    """
        Function that allows users to rate a publication
        TODO: Create checking mechanism that will ensure that user did not rated same publication
              multiple times
    """
    publication = get_object_or_404(Publication, id=id)
    publication.rating = (publication.rated_sum + rate) / (publication.rated_times + 1)
    publication.rated_times += 1
    publication.rated_sum += rate
    publication.save()
    return Response({
        "status": "success",
        "data": PublicationSerializer(publication).data
    }, status=status.HTTP_200_OK)
# ==================================================================================================