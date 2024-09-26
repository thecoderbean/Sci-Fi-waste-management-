from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.
   
class RegisteredUser(AbstractUser):
    img = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    pincode = models.PositiveIntegerField(blank=True, null=True)
    number = models.CharField(max_length=10, unique=True)
    address = models.TextField()

    def __str__(self):
        return self.username