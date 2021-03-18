from django.urls import path
from . import views

urlpatterns = [
     path('', views.HomeView.as_view(), name='home'),
     path('volunteer', views.VolunteerHome.as_view(), name="volunteer-home"),
     path('volunteer/self/<int:id>', views.VolunteerAction.as_view(), name="self-volunteer"),
     path('volunteer/activity/new', views.NewActivity.as_view(), name="new-activity"),
     # Authentication
     path('login', views.LoginView.as_view(), name='login'),
     path('logout', views.LogoutView.as_view(), name='logout')
]
