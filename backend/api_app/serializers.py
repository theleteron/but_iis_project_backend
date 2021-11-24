from rest_framework import serializers
from .models import Library, Publication, Book, PublicationOrder, BookOrder, BookLoan
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

# Publication Serializer
class PublicationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50)
    series = serializers.CharField(max_length=50)
    synopsis = serializers.CharField(max_length=255)
    authors = serializers.CharField(max_length=255)
    language = serializers.CharField(max_length=50)
    ISBN = serializers.CharField(max_length=20, unique=True)
    date_of_publication = serializers.DateTimeField()
    publisher = serializers.CharField(max_length=50)
    genre = serializers.CharField(max_length=50)
    pages = serializers.IntegerField()
    tags = serializers.CharField(max_length=255)
    rating = serializers.FloatField()

    class Meta:
        model = Publication
        fields = ('__all__')

# Book Serializer
class BookSerializer(serializers.ModelSerializer):
    STATES = (
        (1, "New"),
        (2, "Used"),
        (3, "Damaged"),
    )

    publication = serializers.PrimaryKeyRelatedField()
    library = serializers.PrimaryKeyRelatedField()
    condition = serializers.CharField(max_length=30, choices=STATES, default=1)
    section = serializers.IntegerField()
    loaned = serializers.BooleanField(default=False)

    class Meta:
        model = Book
        fields = ('__all__')

# PublicationOrder Serializer
class PublicationOrderSerializer(serializers.ModelSerializer):
    publication         = serializers.PrimaryKeyRelatedField()
    user                = serializers.PrimaryKeyRelatedField()
    date_of_order       = serializers.DateTimeField(auto_now_add=True)
    delivered           = serializers.BooleanField(default=False)
    price               = serializers.FloatField()

    class Meta:
        model = PublicationOrder
        fields = ()

# BookOrder Serializer
class BookOrderSerializer(serializers.ModelSerializer):
    publication_order   = serializers.PrimaryKeyRelatedField()
    number_of_books     = serializers.IntegerField()
    price_per_book      = serializers.FloatField()

    class Meta:
        model = BookOrder
        fields = ('__all__')

# BookLoan Serializer
class BookLoanSerializer(serializers.ModelSerializer):
    user                = serializers.PrimaryKeyRelatedField()
    date_from           = serializers.DateTimeField()
    date_to             = serializers.DateTimeField()
    extension_to        = serializers.DateTimeField()
    fine                = serializers.FloatField(default=0)
    books               = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = BookLoan
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