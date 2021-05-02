from django.contrib import admin
from .models import *

admin.site.register(Profile)
admin.site.register(PetProfile)
admin.site.register(Activity)
admin.site.register(PasswordReset)
admin.site.register(TimeLine)
admin.site.register(Complaints)