from django.shortcuts import get_object_or_404
from rest_condition import And, Or
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api_app.models import Voting
from api_app.permissions import IsAdministrator, IsLibrarian
from api_app.serializers import VotingSerializer

# ================= List information about all votings or just selected one ===================
"""
    Schema for the possisble responses to a request for a publication information
"""
votingGetResponses = {
    "200": openapi.Response(
        description="Retrieval of voting information OK.",
        examples={
            "application/json": {
                "status": "success",
                "data": {
                    "library": "<int>",
                    "publication": "<int>",
                    "votes": "<int>",
                    "completed": "<boolean>"
                }
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
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Voting"],
    method="GET",
    operation_description="Returns list of all voting in the system or just one specified by an id",
    responses=votingGetResponses
)
@api_view(['GET'])
@permission_classes([AllowAny])
def getVoting(request, id=None):
    """
        Function that allows users to list all votings or just selected one
    """
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
# ==================================================================================================

# =================== List information about all votings in specified library ======================
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Voting"],
    method="GET",
    operation_description="Returns list of all voting in the system for the library specified by library id",
    responses=votingGetResponses
)
@api_view(['GET'])
@permission_classes([AllowAny])
def getLibraryVoting(request, id):
    """
        Function that allows users to list votings in specified library
    """
    items = Voting.objects.filter(library=id).filter(completed=False)
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
# ==================================================================================================

# ====================================== Create a new voting =======================================
"""
    Schema for the possisble responses to a request for a voting create
"""
votingPostResponses = {
    "200": openapi.Response(
        description="Creation of voting successfull!",
        examples={
            "application/json": {
                "status": "success"
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
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Voting"],
    method="POST",
    operation_description="Allows user create new voting",
    request_body=VotingSerializer,
    responses=votingPostResponses
)
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian))])
def createVoting(request):
    """
        Function that allows users with selected roles to create a new votings.
    """
    serializer = VotingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
           "status": "success"
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "status": "error",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
# ==================================================================================================

# ======================================== Vote for a voting =======================================
"""
    Schema for the possisble responses to a request for a vote
"""
votingPutResponses = {
    "200": openapi.Response(
        description="Voting updated!",
        examples={
            "application/json": {
                "status": "success"
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
        description="Unauthorized to do the operation.",
        examples={
            "application/json": {
                "detail": "Authentication credentials were not provided."
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
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Voting"],
    method="PUT",
    operation_description="Allows user to vote to buy publication to library",
    responses=votingPutResponses
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def vote(request, id):
    """
        Function that allows users to vote for a publication
    """
    voting = get_object_or_404(Voting, id=id)
    if voting.completed:
        return Response({
            "status": "not_availiable"
        },status=status.HTTP_404_NOT_FOUND)
    if request.user in voting.users.all():
        return Response({
            "status": "error",
            "data": "You have already voted!"
        },status=status.HTTP_401_UNAUTHORIZED)
    voting.votes += 1
    voting.users.add(request.user)
    voting.save()
    return Response({
        "status": "success",
        "data": VotingSerializer(voting).data
    }, status=status.HTTP_200_OK)
# ==================================================================================================

# ========================================== End a voting ==========================================
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Voting"],
    method="PUT",
    operation_description="Allows user to end voting",
    responses=votingPutResponses
)
@api_view(['PUT'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian))])
def voteEnd(request, id):
    """
        Function that allows users with selected roles delete voting
    """
    voting = get_object_or_404(Voting, id=id)
    voting.completed=True
    voting.save()
    # Create new voting after ending the last one
    new_voting = Voting()
    new_voting.library = voting.library
    new_voting.publication = voting.publication
    new_voting.votes = 0
    new_voting.save()
    return Response({
        "status": "success",
        "data": VotingSerializer(voting).data
    }, status=status.HTTP_200_OK)
# ==================================================================================================

# ====================================== Delete a voting ===========================================
"""
    Schema for the possible responses to a delete request for a vote
"""
votingDeleteResponses = {
    "200": openapi.Response(
        description="Voting deleted!",
        examples={
            "application/json": {
                "status": "success"
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
        description="Unauthorized to do the operation.",
        examples={
            "application/json": {
                "detail": "Authentication credentials were not provided."
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
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Voting"],
    method="DELETE",
    operation_description="Allows administrator to delete voting",
    responses=votingDeleteResponses
)
@api_view(['DELETE'])
@permission_classes([And(IsAuthenticated, IsAdministrator)])
def voteDelete(request, id):
    """
        Function that allows administrator to end voting
    """
    voting = get_object_or_404(Voting, id=id).delete()
    # Create new voting after ending the last one
    return Response({
        "status": "success"
    }, status=status.HTTP_200_OK)

# ==================================================================================================
