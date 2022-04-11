from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


# Create your models here.
class Region(models.Model):

    class Regions(models.TextChoices):
        dk1 = 'dk1'
        dk2 = 'dk2'

    name = models.CharField(max_length=5, unique=True, choices=Regions.choices)


class CustomUserManager(BaseUserManager):
    """
        Custom user model manager where email is the unique identifiers
        for authentication instead of usernames.
        """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    username_validator = None
    username = None
    email = models.EmailField(verbose_name='email', max_length=255, unique=True, default='')
    password = models.CharField(max_length=255)
    default_price = models.FloatField(null=True)
    default_emission = models.FloatField(null=True)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['region', 'default_price', 'default_emission']

    objects = CustomUserManager()


class Device(models.Model):
    name = models.CharField(max_length=255)
    ready = models.BooleanField()
    completed_before = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    time_to_complete = models.IntegerField(null=True)
    allowed_on_time = models.CharField(max_length=15)
    energy_consumption = models.FloatField()
    preferred_price = models.FloatField()
    preferred_emission = models.FloatField()
    bluetooth_address = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Value(models.Model):
    pref_max_value = models.FloatField()
    pref_min_value = models.FloatField()
    value = models.FloatField(null=True)
    increase_decrease = models.BooleanField(blank=False, null=True)
    device = models.OneToOneField(Device, on_delete=models.CASCADE, null=True)


class PrognosedPrice(models.Model):
    HourDK = models.DateTimeField(blank=False, auto_now=False, auto_now_add=False)
    PriceArea = models.CharField(max_length=5, blank=False, default='')
    SpotPriceDKK = models.FloatField(blank=False)
    # region = models.ForeignKey(Region, on_delete=models.CASCADE)


class Emission(models.Model):
    Minutes5DK = models.DateTimeField(blank=False, auto_now=False, auto_now_add=False)
    CO2Emission = models.IntegerField(blank=False)
    PriceArea = models.CharField(max_length=5, blank=False, default='')

    class Meta:
        unique_together = ['Minutes5DK', 'PriceArea']


class PrognosedEmission(models.Model):
    Minutes5DK = models.DateTimeField(blank=False, auto_now=False, auto_now_add=False)
    CO2Emission = models.IntegerField(blank=False)
    PriceArea = models.CharField(max_length=5, blank=False, default='')

    class Meta:
        unique_together = ['Minutes5DK', 'PriceArea']
