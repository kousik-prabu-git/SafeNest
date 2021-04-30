from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime


class HomeView(View):
    def get(self, request):
        context = {
            "volunteers" : len(Profile.objects.filter(isVolunteer=True)),
            "donors" : len(Profile.objects.filter(isDonor=True)),
            "adoptions" : len(PetProfile.objects.filter(adopted=True)),
        }
        return render(request, 'home.html', context)

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            "profile" : Profile.objects.get(user__username=request.user.username),
            "timeLine" : TimeLine.objects.filter(user=request.user.username).order_by('-timeStamp')
        }
        return render(request, 'profile.html', context)

class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            "profile" : Profile.objects.get(user__username=request.user.username)
        }
        return render(request, 'editprofile.html', context)

    def post(self, request):
        profile = Profile.objects.get(user__username=request.user.username)
        user = profile.user
        user.first_name = request.POST.get('profileName')
        user.save()
        profile.dateofBirth = datetime.datetime.strptime(request.POST.get('dateofBirth'), '%Y-%m-%d')
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.city = request.POST.get('city')
        profile.profilePicture = request.POST.get('profilePicture')
        profile.license = request.POST.get('license')
        profile.panCard = request.POST.get('panCard')
        profile.vehicleType = request.POST.get('vehicleType')
        profile.aadhar = request.POST.get('aadhar')
        profile.save()
        messages.success(request, 'Profile has been updated!')
        return redirect('profile')

class LoginView(View):
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'You have logged in successfully')
            return redirect('profile')
        else:
            messages.success(request, 'Invalid login details')
        return redirect('home')

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('home')

class VolunteerHome(View):
    def get(self, request):
        context = {
            "activities" : Activity.objects.all(),
        }
        return render(request, 'volunteer/home.html', context)

class VolunteerAction(View):
    def get(self, request, id):
        activity = Activity.objects.get(id=id)
        if request.user.is_authenticated:
            user = Profile.objects.get(user__username=request.user.username)
            print(user.license, user.aadhar)
            if user.license != '' and user.aadhar != '':
                if not user.isVolunteer:
                    user.isVolunteer = True
                    user.save()
                activity.volunteer = user.user.username
                timeLine = TimeLine()
                timeLine.user = user.user.username
                timeLine.type = 'Volunteer'
                timeLine.description = 'Volunteered at %s for a %s %s in the condition of %s' %(activity.location, activity.breed, activity.pet, activity.condition)
                timeLine.save()
                activity.actionStamp = timezone.now()
                activity.save()
                messages.success(request, 'You are now volunteering the activity!')
            else:
                messages.success(request, 'Please update your profile with Aadhar and License Details')
        return redirect('volunteer-home')

class NewActivity(View):
    def post(self, request):
        activity = Activity()
        activity.reporter = request.user.username
        activity.pet = request.POST.get('pet')
        activity.breed = request.POST.get('breed')
        activity.condition = request.POST.get('condition')
        activity.location = request.POST.get('location')
        activity.save()
        timeLine = TimeLine()
        timeLine.user = request.user.username
        timeLine.type = 'Volunteer'
        timeLine.description = 'Reached out for help at %s for a %s %s in the condition of %s' %(request.POST.get('location'), request.POST.get('breed'), request.POST.get('pet'), request.POST.get('condition'))
        timeLine.save()
        return redirect('volunteer-home')

class AdoptView(View):
    def get(self, request):
        context = {
            "pets" : PetProfile.objects.filter(adopted=False)
        }
        return render(request, 'adopt/home.html', context)

class AdoptPetView(View):
    def get(self, request, id):
        user = Profile.objects.get(user__username=request.user.username)
        if user.aadhar != '':
            if not user.isAdopter:
                user.isAdopter = True
                user.save()
            pet = PetProfile.objects.get(id=id)
            pet.adopted = True
            pet.save()
            timeLine = TimeLine()
            timeLine.user = request.user.username
            timeLine.type = 'Adopte'
            timeLine.description = 'Adopted %s, a %s %s' %(pet.name, pet.sex, pet.breed)
            timeLine.save()
            messages.success(request, 'You have successfully adopted %s' %(pet.name))
        else:
            messages.success(request, 'Please update your profile with Aadhar Details')
        return redirect('adoption-page')

class DonatePaymentPageView(View):
    def get(self, request):
        return render(request, 'donate/home.html')
    
    def post(self, request):
        if request.POST.get('otp') == '123456':
            profile = Profile.objects.get(user__username=request.user.username)
            if profile.aadhar != '' and profile.panCard != '':
                profile.donatedAmount += float(request.POST.get('amount'))
                if not profile.isDonor:
                    profile.isDonor = True
                profile.save()
                timeLine = TimeLine()
                timeLine.user = request.user.username
                timeLine.type = 'Donate'
                timeLine.description = 'Donated ₹ %s' %(float(request.POST.get('amount')))
                timeLine.save()
                messages.success(request, 'Donation successful')
            else:
                messages.success(request, 'Please your profile with Aadhar and Pan Card Details')
        else:
            messages.success(request, 'Payment Failed')
        return redirect('profile')