from django.db import models

# Create your models here.
class Library(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=255)
    city = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    zip_code = models.IntegerField()