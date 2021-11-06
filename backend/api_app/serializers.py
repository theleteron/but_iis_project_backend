from django.db.models import fields
from rest_framework import serializers
from .models import Library
from django.contrib.auth.models import User

# Library Serializer
class LibrarySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=200)
    street = serializers.CharField(max_length=200)
    zip_code = serializers.IntegerField()

    class Meta:
        model = Library
        fields = ('__all__')


##!!! Following are taken from https://studygyaan.com/django/django-rest-framework-tutorial-register-login-logout
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user

##!!!