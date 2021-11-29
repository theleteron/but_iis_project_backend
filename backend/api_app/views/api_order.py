from django.shortcuts import get_object_or_404
from rest_condition import And, Or
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api_app.models import Book, BookOrder, PublicationOrder
from api_app.permissions import IsAdministrator, IsDistributor, IsLibrarian
from api_app.serializers import BookOrderSerializer, PublicationOrderCreateByAdmin, PublicationOrderCreateByLibrarian, PublicationOrderSerializer

"""
    Schema for the possisble responses to a request for a order information
"""
orderGetResponses = {
    "200": openapi.Response(
        description="Publication order data retrieved successfully!",
        examples={
            "application/json": {
                "status": "success",
                "data": [
                    {
                        "id": "<int>",
                        "publication": "<int>",
                        "library": "<int>",
                        "user": "<int>",
                        "date_of_order": "<date_time>",
                        "delivered": "<boolean>",
                        "price": "<float>"
                    }
                ]
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
# ===================== List information about all orders or just selected one =====================
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Order"],
    method="GET",
    operation_description="Returns list of all orders in the system or just information about the one specified by the id.",
    responses=orderGetResponses
)
@api_view(['GET'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian, IsDistributor))])
def getOrder(request, id=None):
    """
        Function that allows users with selected roles to list publication orders.
    """
    if id:
        item = get_object_or_404(PublicationOrder, pk=id)
        related = get_object_or_404(BookOrder, publication_order=id)
        serializer = PublicationOrderSerializer(item)
        serializer_r = BookOrderSerializer(related)
        return Response({
            "status": "success",
            "data": serializer.data,
            "data_details": serializer_r.data
        }, status=status.HTTP_200_OK)

    items = PublicationOrder.objects.all()
    serializer = PublicationOrderSerializer(items, many=True)
    return Response({
        "status": "success",
        "data": serializer.data
    }, status=status.HTTP_200_OK)
# ==================================================================================================

# ==================== List information about all orders specified by a library ====================
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Order"],
    method="GET",
    operation_description="Returns list of all orders in the system for the library specified by library id",
    responses=orderGetResponses
)
@api_view(['GET'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian, IsDistributor))])
def getOrderLibrarySpecified(request, id):
    """
        Function that allows users with selected roles to list publication orders filtered by library.
    """
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
# ==================================================================================================

# ==================== List information about all orders specified by a user =======================
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Order"],
    method="GET",
    operation_description="Returns list of all orders in the system specified by user id",
    responses=orderGetResponses
)
@api_view(['GET'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian, IsDistributor))])
def getOrderUserSpecified(request, id):
    """
        Function that allows users with selected roles to list publication orders filtered by a user.
    """
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
# ==================================================================================================

# ============== List information about all orders specified by a library and status ===============
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Order"],
    method="GET",
    operation_description="Returns list of all orders in the system that were or were not delivered",
    responses=orderGetResponses
)
@api_view(['GET'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsLibrarian, IsDistributor))])
def getOrderDelivered(request, delivered, id=None):
    """
        Function that allows users with selected roles to list publication orders filtered by library and status.
    """
    if delivered not in [0, 1]:
            return Response({
                "status": "error",
                "data": "Delivered flag must be 0 (false) or 1 (true)!"
            }, status=status.HTTP_400_BAD_REQUEST)
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
# ==================================================================================================

# ============================== Create a new order for a publications =============================
"""
    Schema for the possisble responses to a request for a publication order creation
"""
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
"""
    Settings for Swagger OpenAPI documentation
"""
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
    """
        Function that allows users with selected roles to create publication orders.
    """
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
# ==================================================================================================

# =================================== Mark an order as delivered ===================================
"""
    Schema for the possisble responses to a request for a publication order deliver status change
"""
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
"""
    Settings for Swagger OpenAPI documentation
"""
@swagger_auto_schema(
    tags=["Order"],
    method="POST",
    operation_description="Set order specified by PublicationOrder ID as delivered",
    responses=orderPostDeliverResponses
)
@api_view(['POST'])
@permission_classes([And(IsAuthenticated, Or(IsAdministrator, IsDistributor))])
def deliverOrder(request, id):
    """
        Function that allows users with selected roles to mark publication orders as delivered.
    """
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
# ==================================================================================================