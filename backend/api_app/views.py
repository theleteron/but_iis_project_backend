from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LibrarySerializer
from .models import Library

# Create your views here.
class LibraryViews(APIView):
    def post(self, request):
        serializer = LibrarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, id=None):
        if id:
            item = Library.objects.get(id=id)
            serializer = LibrarySerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        
        items = Library.objects.all()
        serializer = LibrarySerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)