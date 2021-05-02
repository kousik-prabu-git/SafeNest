from django.urls import path
from . import views

urlpatterns = [
     path('', views.HomeView.as_view(), name='home'),
     path('profile', views.ProfileView.as_view(), name='profile'),
     path('profile/edit', views.ProfileEditView.as_view(), name='profile-edit'),
     path('volunteer', views.VolunteerHome.as_view(), name="volunteer-home"),
     path('volunteer/self/<int:id>', views.VolunteerAction.as_view(), name="self-volunteer"),
     path('volunteer/activity/new', views.NewActivity.as_view(), name="new-activity"),
     path('adopt', views.AdoptView.as_view(), name='adoption-page'),
     path('adopt/<id>', views.AdoptPetView.as_view(), name='adoption-view'),
     path('donate', views.DonatePaymentPageView.as_view(), name='donate-view'),
     # Authentication
     path('login', views.LoginView.as_view(), name='login'),
     path('logout', views.LogoutView.as_view(), name='logout'),
     path('signup', views.SignUpView.as_view(), name='signup'),
     path('password/<key>', views.PasswordSetPageView.as_view(), name='password'),
     path('forgetpassword', views.PasswordResetPageView.as_view(), name='forgotpassword')
]
