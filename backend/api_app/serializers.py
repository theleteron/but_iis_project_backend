from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Account, Library, Publication, Book, PublicationOrder, BookOrder, BookLoan
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.conf import settings

User = get_user_model()

# LibraryAPI ==========================================================================================================
# Serializer for Library model
class LibrarySerializer(serializers.ModelSerializer):
    name                    = serializers.CharField(max_length=200)
    description             = serializers.CharField(max_length=255)
    city                    = serializers.CharField(max_length=200)
    street                  = serializers.CharField(max_length=200)
    zip_code                = serializers.IntegerField()

    class Meta:
        model = Library
        fields = ('__all__')
# =====================================================================================================================


# PublicationAPI ======================================================================================================
# Serializer for Publication model
class PublicationSerializer(serializers.ModelSerializer):
    name                    = serializers.CharField(max_length=50)
    series                  = serializers.CharField(max_length=50)
    synopsis                = serializers.CharField(max_length=255)
    authors                 = serializers.CharField(max_length=255)
    language                = serializers.CharField(max_length=50)
    ISBN                    = serializers.CharField(max_length=20)
    date_of_publication     = serializers.DateTimeField()
    publisher               = serializers.CharField(max_length=50)
    genre                   = serializers.CharField(max_length=50)
    pages                   = serializers.IntegerField()
    tags                    = serializers.CharField(max_length=255)
    rating                  = serializers.FloatField()
    availiable_at           = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Publication
        fields = ('__all__')
# =====================================================================================================================


# BookAPI =============================================================================================================
# Serializer for Book model
class BookSerializer(serializers.ModelSerializer):
    publication             = serializers.PrimaryKeyRelatedField(read_only=True)
    library                 = serializers.PrimaryKeyRelatedField(read_only=True)
    condition               = serializers.CharField(max_length=30)
    section                 = serializers.IntegerField()
    loaned                  = serializers.BooleanField(default=False)

    class Meta:
        model = Book
        fields = ('__all__')
# =====================================================================================================================


# OrderAPI ============================================================================================================
# Serializer for creating PublicationOrder & BookOrder as Librarian
class PublicationOrderCreateByLibrarian(serializers.ModelSerializer):
    publication             = serializers.IntegerField()
    date_of_order           = serializers.DateTimeField()
    delivered               = serializers.BooleanField(default=False)
    number_of_books         = serializers.IntegerField()
    price_per_book          = serializers.FloatField()
    total_price             = serializers.FloatField()

    class Meta:
        model = PublicationOrder
        fields = (
            'publication', 
            'date_of_order', 
            'delivered', 
            'number_of_books', 
            'price_per_book', 
            'total_price'
        )

    def create(self, validated_data):
        publication_order = PublicationOrder()
        publication_order.publication = get_object_or_404(Publication, id=validated_data['publication'])
        publication_order.library = validated_data['library']
        publication_order.user = validated_data['creator']
        publication_order.date_of_order = validated_data['date_of_order']
        publication_order.price = validated_data['total_price']
        publication_order.save()
        book_order = BookOrder()
        book_order.publication_order = publication_order
        book_order.number_of_books = validated_data['number_of_books']
        book_order.price_per_book = validated_data['price_per_book']
        book_order.save()
        return book_order

# Serializer for creating PublicationOrder & BookOrder as Administator
class PublicationOrderCreateByAdmin(serializers.ModelSerializer):
    publication             = serializers.IntegerField()
    library                 = serializers.IntegerField()
    date_of_order           = serializers.DateTimeField()
    delivered               = serializers.BooleanField(default=False)
    number_of_books         = serializers.IntegerField()
    price_per_book          = serializers.FloatField()
    total_price             = serializers.FloatField()

    class Meta:
        model = PublicationOrder
        fields = (
            'publication', 
            'library', 
            'date_of_order', 
            'delivered', 
            'number_of_books', 
            'price_per_book', 
            'total_price'
        )

    def create(self, validated_data):
        publication_order = PublicationOrder()
        publication_order.publication = get_object_or_404(Publication, id=validated_data['publication'])
        publication_order.library = get_object_or_404(Library, id=validated_data['library'])
        publication_order.user = validated_data['creator']
        publication_order.date_of_order = validated_data['date_of_order']
        publication_order.price = validated_data['total_price']
        publication_order.save()
        book_order = BookOrder()
        book_order.publication_order = publication_order
        book_order.number_of_books = validated_data['number_of_books']
        book_order.price_per_book = validated_data['price_per_book']
        book_order.save()
        return book_order

# Serializer for PublicationOrder model
class PublicationOrderSerializer(serializers.ModelSerializer):
    publication             = serializers.PrimaryKeyRelatedField(read_only=True)
    library                 = serializers.PrimaryKeyRelatedField(read_only=True)
    user                    = serializers.PrimaryKeyRelatedField(read_only=True)
    date_of_order           = serializers.DateTimeField()
    delivered               = serializers.BooleanField(default=False)
    price                   = serializers.FloatField()

    class Meta:
        model = PublicationOrder
        fields = ('__all__')

# Serializer for BookOrder model
class BookOrderSerializer(serializers.ModelSerializer):
    publication_order       = serializers.PrimaryKeyRelatedField(read_only=True)
    number_of_books         = serializers.IntegerField()
    price_per_book          = serializers.FloatField()

    class Meta:
        model = BookOrder
        fields = ('__all__')
# =====================================================================================================================


# BookLoanAPI =========================================================================================================
# Serializer for BookLoan model
class BookLoanSerializer(serializers.ModelSerializer):
    user                    = serializers.PrimaryKeyRelatedField(read_only=True)
    loans                   = serializers.PrimaryKeyRelatedField(read_only=True, allow_null=True)
    receives                = serializers.PrimaryKeyRelatedField(read_only=True, allow_null=True)
    date_from               = serializers.DateTimeField()
    date_to                 = serializers.DateTimeField()
    extension_to            = serializers.DateTimeField(allow_null=True)
    fine                    = serializers.FloatField(default=0)
    books                   = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = BookLoan
        fields = ('__all__')
# =====================================================================================================================


# UserAPI =============================================================================================================
# Serializer for User model
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

# Serializer for update of the User as normal user
class UserNormalEditSerializer(serializers.ModelSerializer):
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
                'phone'
            )

# Serializer for update of the User as Administrator
class UserAdminEditSerializer(serializers.ModelSerializer):
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
            )
# =====================================================================================================================


# AdminAPI ============================================================================================================
# Serializer for AdminKey
class AdminKeySerializer(serializers.Serializer):
    key = serializers.CharField(max_length=128)

    def validate(self, data):
        if data['key'] == settings.ADMIN_KEY:
            return True
        return False
# =====================================================================================================================


# AuthenticationAPI ===================================================================================================
# Serializer for Login Request
class LoginSerializer(serializers.Serializer):
    username = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid Details.")

# Serializer for Registration Request
class RegisterSerializer(serializers.ModelSerializer):
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
            'password'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

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
# =====================================================================================================================