# Import Begin #
from django.db import models
# Import End #

# Create your models here.
class UserSignUp(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    profile_picture = models.ImageField()
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=10)
    email = models.EmailField()
    address = models.TextField()

