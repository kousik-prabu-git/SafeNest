from django.db import models
from django.contrib.auth.models import *
import uuid

class PetProfile(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField(default=0)
    breed = models.CharField(max_length=100)
    color = models.CharField(max_length=30)
    height = models.CharField(max_length=10)
    weight = models.CharField(max_length=10)
    lastUpdated = models.DateTimeField(auto_now=True)
    description = models.TextField()
    image = models.URLField()
    sex = models.CharField(max_length=10)
    adopted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Activity(models.Model):
    pet = models.CharField(max_length=255)
    breed = models.CharField(max_length=100)
    location = models.TextField()
    volunteer = models.CharField(max_length=255, blank=True)
    condition = models.TextField()
    images = models.TextField()
    status = models.BooleanField(default=False)
    reporter = models.CharField(max_length=255)
    timeStamp = models.DateTimeField(auto_now_add=True)
    actionStamp = models.DateTimeField(blank=True, null=True)
    closeStamp = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.pet

    class Meta:
        ordering = ['-timeStamp', '-actionStamp', '-closeStamp']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    isVolunteer = models.BooleanField(default=False)
    isDonor = models.BooleanField(default=False)
    isAdopter = models.BooleanField(default=False)
    adoptedPets = models.ManyToManyField(PetProfile, blank=True)
    donatedAmount = models.FloatField(default=0)
    activities = models.ManyToManyField(Activity, blank=True)
    dateofBirth = models.DateField() #age
    phone = models.CharField(max_length=12)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=200)
    license = models.CharField(max_length=30)
    vehicleType = models.CharField(max_length=30)
    aadhar = models.CharField(max_length=16)
    panCard = models.CharField(max_length=20)
    donorSince = models.DateField(null=True, blank=True)
    donatedAmount = models.FloatField(default=0)
    profilePicture = models.CharField(max_length=2000)

    def __str__(self):
        return self.user.username

class TimeLine(models.Model):
    user = models.CharField(max_length=255)
    description = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True)
