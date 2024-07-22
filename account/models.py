from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import pyotp
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


class CustomUserManager(BaseUserManager):
    def create_user(self, username, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number field must be set')
        user = self.model(username=username, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, phone_number, password, **extra_fields)


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    otp_seed = models.CharField(max_length=16, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.otp_seed is None:
            self.otp_seed = pyotp.random_base32()
        super().save(*args, **kwargs)

    def generate_otp(self):
        if not self.otp_seed:
            self.otp_seed = pyotp.random_base32()
            self.save()
        totp = pyotp.TOTP(self.otp_seed)
        return totp.now()

    def verify_otp(self, otp):
        totp = pyotp.TOTP(self.otp_seed)
        return totp.verify(otp)

    def __str__(self):
        return self.username


class SMSRequest(models.Model):
    status_choices = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed')
    ]

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    task_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=status_choices, default='pending')
    threshold = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(settings.OTP_THRESHOLD_LIMIT)]
    )
