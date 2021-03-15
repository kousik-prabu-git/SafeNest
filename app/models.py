from django.db import models
from django.contrib.auth.models import *


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    isVolunteer = models.BooleanField(default=False)
    isDonor = models.BooleanField(default=False)
    isAdopter = models.BooleanField(default=False)
