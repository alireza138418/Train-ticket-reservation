from django.contrib.admin import ModelAdmin as BaseModelAdmin
from django.contrib import admin
from django.utils.translation import gettext as _
from .models import *

class UserModelAmin(BaseModelAdmin):
    ordering = ['id']
    list_display = ['email' , 'f_name' , 'l_name']
    fieldsets = (
        (_('Login Information') , {'fields': ('email' , 'password')}),
        (_('Personal Information'), {'fields': ('f_name', 'l_name', 'phone_number')}),
        (_('Permission'), {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        (_('Dates'), {'fields': ('birth_date', 'last_login')}),
    )

admin.site.register(User , UserModelAmin)
admin.site.register(Company)
admin.site.register(Seat)
admin.site.register(Reception)
admin.site.register(Reservation)
# Register your models here.

