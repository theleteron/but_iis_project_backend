from django.db.models import fields
from rest_framework import serializers
from .models import Library

class LibrarySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=200)
    street = serializers.CharField(max_length=200)
    zip_code = serializers.IntegerField()

    class Meta:
        model = Library
        fields = ('__all__')