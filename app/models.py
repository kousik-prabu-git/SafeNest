from django.db import models
from django.contrib.auth.models import *

class PetProfile(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField(default=0)
    contact = models.CharField(max_length=12)
    address = models.TextField()
    breed = models.CharField(max_length=100)
    color = models.CharField(max_length=30)
    height = models.CharField(max_length=10)
    weight = models.CharField(max_length=10)
    lastUpdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Activity(models.Model):
    pet = models.CharField(max_length=255)
    breed = models.CharField(max_length=100)
    location = models.TextField()
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='Volunteer')
    condition = models.TextField()
    status = models.BooleanField(default=False)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Reporter')
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
    adoptedPets = models.ManyToManyField(PetProfile)
    donatedAmount = models.FloatField(default=0)
    activities = models.ManyToManyField(Activity)

    def __str__(self):
        return self.user.username