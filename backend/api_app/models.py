from django.db import models

# Library table
class Library(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    # Address
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    zip_code = models.IntegerField()
