from rest_framework import serializers
from .models import Library
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()

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
        fields = (
                'id',
                'username',
                'email', 
                'first_name', 
                'last_name', 
                'city', 
                'street', 
                'zip_code', 
                'country', 
                'phone', 
                'role', 
                'working_at', 
                'date_joined', 
                'last_login'
            )

class LoginSerializer(serializers.Serializer):
    username = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid Details.")

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'city', 'street', 'zip_code', 'country', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
                validated_data['username'], 
                validated_data['email'], 
                validated_data['first_name'],
                validated_data['last_name'],
                validated_data['city'],
                validated_data['street'],
                validated_data['zip_code'],
                validated_data['country'],
                validated_data['password']
            )

        return user

##!!!