from django.shortcuts import get_object_or_404;
from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from knox.models import AuthToken
from .permissions import IsAdministrator, IsDistributor, IsLibrarian, IsRegistredReader
from .serializers import LibrarySerializer, UserSerializer, LoginSerializer, RegisterSerializer
from .models import Library

# Library API
class LibraryViews(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request):
        serializer = LibrarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, id=None):
        if id:
            item = get_object_or_404(Library, pk=id)
            serializer = LibrarySerializer(item)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        
        items = Library.objects.all()
        serializer = LibrarySerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

###
#   USER AUTH & MANAGEMENT
###

class UserAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def get(self, request):
        return Response({"user": UserSerializer(self.request.user).data}, status=status.HTTP_200_OK)

##!!! Following are taken from https://studygyaan.com/django/django-rest-framework-tutorial-register-login-logout
# Register API
class RegisterAPI(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny, ]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

##!!!