from django.db import models
from django.contrib.auth.models import AbstractUser


class AccountType(models.TextChoices):
    SUPERVISOR = 'SUPERVISOR', 'Supervisor'
    ADMIN = 'ADMIN', 'Admin'
    COLLECTOR = 'COLLECTOR', 'Collector'
    USER = 'USER', 'User'

class Gender(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'
    OTHER = 'O', 'Other'


class UserProfile(AbstractUser):
    avatar = models.ImageField(upload_to='images/users/', default='assets/img/avatar.png')
    description = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.OTHER)
    account_type = models.CharField(max_length=10, choices=AccountType.choices, default=AccountType.USER)
    province = models.CharField(max_length=50,null=False)
    city = models.CharField(max_length=50, null=False)
    role = models.CharField(max_length=50,null=False)

    def __str__(self):
        return self.username
