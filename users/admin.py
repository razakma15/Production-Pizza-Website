# users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username','basket_quantity']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Meal)

""" Updates the admin interface to include the extra user variable "basket_quantity" using
the forms created within forms.py """
