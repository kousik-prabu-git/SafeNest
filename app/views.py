from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from django.core.mail import send_mail
import random

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

class SignUpView(View):
    def post(self, request):
        user = User.objects.filter(username=request.POST.get('username'))
        if len(user) != 0:
            messages.success(request, 'Username already exists. Please login if it is you!')
        else:
            user = User()
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.save()
            profile = Profile()
            profile.user = user
            profile.save()
            password = PasswordReset()
            password.user = user
            password.key = random.randint(10000000, 99999999)
            password.save()
            send_mail(
                'SIGN UP | SUCCESSFULL',
                'Dear %s,\nThis email is to confirm that you have successfully created an account on SAFENEST. We are happy to have you as a part of our community to serve all the lives that needs to be loved. But before that, please set your password so that you can access all the updates in our website.\n\nhttp://localhost:8000/password/%s\n\nThank you for being a part of this community.\n\nRegards,\nSafeNest' %(user.username, password.key),
                'safenestkmm2021@gmail.com',
                [user.email],
                fail_silently=False
            )
            messages.success(request, 'Your account has been created. Please check mail for details!')
        return redirect('home')

class PasswordSetPageView(View):
    def get(self, request, key):
        try:
            token = PasswordReset.objects.get(key=key)
            return render(request, 'password.html')
        except:
            messages.success(request, 'Invalid link!')
            return redirect('home')
    def post(self, request, key):
        if len(request.POST.get('password')) > 7:
            if request.POST.get('password') == request.POST.get('password2'):
                token = PasswordReset.objects.get(key=key)
                user = token.user
                user.set_password(request.POST.get('password'))
                user.save()
                # token.delete()
                messages.success(request, 'Password set successfully')
                return redirect('home')
            else:
                err = 1
        else:
            err = 2
        return render(request, 'password.html', context={"err":err})

class PasswordResetPageView(View):
    def get(self, request):
        return render(request, 'forgetpassword.html')
    
    def post(self, request):
        try:
            user = User.objects.get(username=request.POST.get('username'))
            password = PasswordReset()
            password.user = user
            password.key = random.randint(10000000, 99999999)
            password.save()
            send_mail(
                'SIGN UP | SUCCESSFULL',
                'Dear %s,\nThis email is to confirm that you have successfully created an account on SAFENEST. We are happy to have you as a part of our community to serve all the lives that needs to be loved. But before that, please set your password so that you can access all the updates in our website.\n\nhttp://localhost:8000/password/%s\n\nThank you for being a part of this community.\n\nRegards,\nSafeNest' %(user.username, password.key),
                'safenestkmm2021@gmail.com',
                [user.email],
                fail_silently=False
            )
            messages.success(request, 'Password set link has been sent to the email ID')
        except:
            messages.success(request, 'Invalid email ID')
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
            if user.license != '' and user.aadhar != '' and user.vehicleType != '':
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
        profile = Profile.objects.get(user__username=request.user.username)
        if profile.aadhar == '' and profile.panCard == '':
            messages.success(request, 'Please your profile with Aadhar and Pan Card Details')
            return redirect('profile')
        else:
            return render(request, 'donate/home.html')
    
    def post(self, request):
        if request.POST.get('otp') == '123456':
            profile = Profile.objects.get(user__username=request.user.username)
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
            messages.success(request, 'Payment Failed')
        return redirect('profile')

class ComplaintRegister(View):
    def post(self, request):
        complain = Complaints()
        complain.name = request.POST.get('name')
        complain.email = request.POST.get('email')
        complain.complaint = request.POST.get('complaint')
        complain.save()
        messages.success(request, 'Your complaint has been registered!')
        return redirect('volunteer-home')