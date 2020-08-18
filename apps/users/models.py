from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import SET_NULL, CASCADE

from apps.base.models import HouseModel
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class MyUserManager(BaseUserManager):
    def create_user(self, email, phone, password, is_staff=False, is_active=False, is_admin=False, trial=True):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not phone:
            raise ValueError("Users must have a phone number")
        if not password:
            raise ValueError("Users must have a password")

        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
        )

        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.active = is_active
        user.subscribe_trial = trial
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, phone, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            phone=phone,
            is_staff=True
        )
        return user

    def create_superuser(self, email, phone, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            phone=phone,
            is_admin=True
        )
        return user


# Create your models here.
class User(AbstractBaseUser):
    phone_regex = RegexValidator(regex=r"^\+?1?\d{9,14}$",
                                 message="Phone number must be entered in the format: '+999999999'. Up to 14 digits "
                                         "allowed. ")
    phone = models.CharField(validators=[phone_regex], max_length=15, unique=True)
    name = models.CharField(max_length=40, blank=True, null=True)
    email = models.EmailField(unique=True)
    surname = models.CharField(max_length=40, blank=True, null=True)
    is_subscribe = models.BooleanField(default=False)
    subscribe_days_count = models.IntegerField(default=0)
    subscribe_hours_count = models.IntegerField(default=0, validators=[
        MinValueValidator(0),
        MaxValueValidator(24)
    ])
    watched_list = models.ManyToManyField(HouseModel, related_name='watched_list', blank=True, null=True)
    fav_list = models.ManyToManyField(HouseModel, related_name='fav_list', blank=True, null=True)
    ignore_list = models.ManyToManyField(HouseModel, related_name='ignore_list', blank=True, null=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_partner = models.BooleanField(default=False)
    referral_code = models.IntegerField(default=0, null=True)
    parent_referral = models.ForeignKey('self', blank=True, null=True, on_delete=SET_NULL)
    all_discount_count = models.IntegerField(default=0, validators=[
        MinValueValidator(0),
        MaxValueValidator(100)])
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email']
    objects = MyUserManager()

    def __str__(self):
        return self.email + self.phone

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.admin


class PhoneOTP(models.Model):
    phone_regex = RegexValidator(regex=r"^\+?1?\d{9,14}$",
                                 message="Phone number must be entered in the format: '+999999999'. Up to 14 digits "
                                         "allowed. ")
    phone = models.CharField(validators=[phone_regex], max_length=15, unique=True)
    otp = models.CharField(max_length=9, blank=True, null=True)
    count = models.IntegerField(default=0, help_text='Num of OTP send')
    validate = models.BooleanField(default=False)

    def __str__(self):
        return str(self.phone) + ' is_sent ' + str(self.otp)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    days = models.IntegerField(default=0)
    payment_id = models.CharField(max_length=60)
    is_success = models.BooleanField(default=False)
