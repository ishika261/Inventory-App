from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

from django.core.validators import EmailValidator
from django.db.models.fields import NullBooleanField
from django.utils.deconstruct import deconstructible


@deconstructible
class WhitelistEmailValidator(EmailValidator):

    def validate_domain_part(self, domain_part):
        return False

    def __eq__(self, other):
        return isinstance(other, WhitelistEmailValidator) and super().__eq__(other)


def nameFile(instance, filename):
    return '/'.join(['images', str(instance.name), filename])


def itemNameFile(instance, filename):
    return '/'.join(['images', str(instance.item_name), filename])


class UserProfileManager(BaseUserManager):
    """Manager for user-profile"""

    def create_user(self, email, name, profile_img, password=None):
        """Create a new user-profile"""
        if not email:
            raise ValueError("User must have email address")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, profile_img=profile_img)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, profile_img=None, password=None):
        """Create and save a new superuser with given details"""
        #user = self.create_user(email, name, profile_img, password)

        if not email:
            raise ValueError("User must have email address")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, profile_img=profile_img)

        user.set_password(password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):

    """database model for users in the system"""
    email = models.EmailField(max_length=255,
                              unique=True,
                              validators=[WhitelistEmailValidator(whitelist=['iiti.ac.in'])])
    name = models.CharField(max_length=255)
    profile_img = models.ImageField(upload_to=nameFile, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_name(self):
        """Retrieve full_name of user"""
        return self.name

    def __str__(self):
        """Retrieve string representation of our user"""
        return self.email


class InventoryItem(models.Model):
    """Model for Inventory-item"""
    owner_club = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    item_name = models.CharField(max_length=100)
    item_description = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    item_img = models.ImageField(upload_to=itemNameFile, blank=True, null=True)
    total_quantity = models.PositiveIntegerField()
    avl_quantity = models.PositiveIntegerField()

    def __str__(self):
        """Return the model as string"""
        return self.item_name


class Event(models.Model):
    owner_club = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    event_name = models.CharField(max_length=100)
    event_description = models.CharField(max_length=255)
    status = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        """Return the model as string"""
        return self.event_name


class EventInventoryRelationship(models.Model):
    event_id = models.ForeignKey(
        to='Event',
        on_delete=models.CASCADE
    )
    inventory_id = models.ForeignKey(
        to='InventoryItem',
        on_delete=models.CASCADE
    )
    req_quantity = models.PositiveIntegerField()
    approval_status = models.CharField(max_length=100, default='Pending')
