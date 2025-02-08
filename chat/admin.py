from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(CustomUser, UserAdmin)