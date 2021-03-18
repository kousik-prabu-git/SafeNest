from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')

class LoginView(View):
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'You have logged in successfully')
            return redirect('home')
        else:
            messages.success(request, 'Invalid login details')
        return redirect('home')

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('home')

class VolunteerHome(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            "activities" : Activity.objects.all(),
        }
        return render(request, 'volunteer/home.html', context)

class VolunteerAction(LoginRequiredMixin, View):
    def get(self, request, id):
        activity = Activity.objects.get(id=id)
        activity.volunteer = User.objects.get(username=request.user.username)
        activity.actionStamp = timezone.now()
        activity.save()
        return redirect('volunteer-home')

class NewActivity(LoginRequiredMixin, View):
    def post(self, request):
        activity = Activity()
        activity.reporter = User.objects.get(username=request.user.username)
        activity.pet = request.POST.get('pet')
        activity.breed = request.POST.get('breed')
        activity.condition = request.POST.get('condition')
        activity.location = request.POST.get('location')
        activity.save()
        return redirect('volunteer-home')