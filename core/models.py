from django.db import models
from django.contrib.auth.models import AbstractUser
import random
import string
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class VerificationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_code():
        return ''.join(random.choices(string.digits, k=6))