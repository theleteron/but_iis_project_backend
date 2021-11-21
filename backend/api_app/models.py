from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

###
#   DATABASE STRUCTURE
###
# Library table

class Library(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    # Address
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    zip_code = models.IntegerField()

###
#   USER DATA & MANAGMENT
###

class AccountManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, city, street, zip_code, country, password = None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")
        if not first_name:
            raise ValueError("Users must have an first name")
        if not last_name:
            raise ValueError("Users must have an last name")
        if not city:
            raise ValueError("Users must have an city")
        if not street:
            raise ValueError("Users must have an street")
        if not zip_code:
            raise ValueError("Users must have an zip code")
        if not country:
            raise ValueError("Users must have an country")
        
        user = self.model(
                username=username,
                email=self.normalize_email(email),
                first_name=first_name,
                last_name=last_name,
                city=city,
                street=street,
                zip_code=zip_code,
                country=country,
            )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, first_name, last_name, city, street, zip_code, country, password = None):
        user = self.create_user(
                username=username,
                email=self.normalize_email(email),
                first_name=first_name,
                last_name=last_name,
                city=city,
                street=street,
                zip_code=zip_code,
                country=country,
                password=password,
            )
        
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class Account(AbstractBaseUser):
    # Main user identification
    username        = models.CharField(max_length=30, unique=True)
    email           = models.EmailField(verbose_name="email", max_length=60, unique=True)
    # User details
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    city            = models.CharField(max_length=50)
    street          = models.CharField(max_length=50)
    zip_code        = models.IntegerField()
    country         = models.CharField(max_length=50)
    phone           = models.IntegerField(null=True)
    # Access details
    ROLE_OPTIONS = (
        (1, "Registred reader"),
        (2, "Distributor"),
        (3, "Librarian"),
        (4, "Administrator"),
    )
    role            = models.CharField(verbose_name="role", max_length=30, choices=ROLE_OPTIONS, default=1)
    working_at      = models.ForeignKey(Library, null=True, on_delete=models.RESTRICT)
    # Other details & flags
    date_joined     = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login      = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_superuser    = models.BooleanField(default=False)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)

    USERNAME_FIELD  = 'email'
    EMAIL_FIELD     = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'city', 'street', 'zip_code', 'country']

    objects = AccountManager()

    def get_full_name(self):
        return self.first_name + self.last_name

    def get_short_name(self):
        return self.first_name