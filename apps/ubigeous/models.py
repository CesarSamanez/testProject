import uuid as uuid_lib

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


# Custom class to manage user creation and authentication
class UserManager(BaseUserManager):
    # Method for creates and saves a regular user
    def _create_user(self, username, name, lastname, email, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username=username,
            name=name,
            lastname=lastname,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.password = password
        user.save(using=self.db)
        return user

    # Method for creating regular users
    def create_user(self, username, name, lastname, email=None, password=None, **extra_fields):
        return self._create_user(username, name, lastname, email, password, False, False, **extra_fields)

    # Method for creating a superuser or admin with elevated privileges
    def create_superuser(self, username, name, lastname, email=None, password=None, **extra_fields):
        return self._create_user(username, name, lastname, email, password, True, True, **extra_fields)


# Definition of the 'User' model
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid_lib.uuid4,  # 128-bit identifier
        editable=False,
        unique=True,
        db_index=True
    )
    username = models.CharField(
        'Username',
        max_length=255,
        blank=False,
        null=True,
        unique=True
    )
    name = models.CharField(
        'Name',
        max_length=255,
        blank=False,
        null=False
    )
    lastname = models.CharField(
        'Lastname',
        max_length=255,
        unique=False,
        blank=True,
        null=True
    )
    email = models.EmailField(
        'Email',
        max_length=255,
        unique=True,
        blank=False,
        null=True
    )
    state = models.BooleanField(
        'State',
        default=True
    )
    created = models.DateTimeField(
        'created_datetime',
        auto_now_add=True,
        blank=False,
        null=False
    )
    updated = models.DateTimeField(
        'updated_datetime',
        auto_now=True,
        blank=False,
        null=False
    )

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)

    # Defining the object manager for the model class
    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name', 'lastname']

    def __str__(self):
        return f'{self.id} - {self.name} - {self.lastname}'

    # Overriding the method to save the encrypted password through django-admin
    def save(self, *args, **kwargs):
        user = super(User, self)
        if User.objects.filter(pk=user.pk).count() > 0:
            _user = User.objects.filter(pk=user.pk)
            if _user[0].password != self.password and self.password.find('_sha256') < 0:
                user.set_password(self.password)
        else:
            user.set_password(self.password)
        user.save(*args, **kwargs)
        return user


# Definition of the 'Region' model
class Region(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=6,
        unique=True
    )
    name = models.CharField(
        'Name',
        max_length=100
    )
    created = models.DateTimeField(
        'Created_datetime',
        auto_now_add=True
    )
    updated = models.DateTimeField(
        'Updated_datetime',
        auto_now=True
    )

    def __str__(self):
        return self.name


# Definition of the 'Province' model
class Province(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=6,
        unique=True
    )
    name = models.CharField(
        'name',
        max_length=255
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        verbose_name='region'
    )
    created = models.DateTimeField(
        'created_datetime',
        auto_now_add=True
    )
    updated = models.DateTimeField(
        'updated_datetime',
        auto_now=True
    )

    def __str__(self):
        return f'{self.name} - {self.region}'


# Definition of the 'District' model
class District(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=6,
        unique=True
    )
    name = models.CharField(
        'name',
        max_length=255
    )
    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        verbose_name='province'
    )
    created = models.DateTimeField(
        'created_datetime',
        auto_now_add=True
    )
    updated = models.DateTimeField(
        'updated_datetime',
        auto_now=True
    )

    def __str__(self):
        return f'{self.name} - {self.province}'
