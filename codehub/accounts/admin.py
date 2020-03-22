from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import User

UserAdmin.list_display = ('id', 'username', 'email', 'is_staff')
UserAdmin.list_filter = ('id', 'username', 'email', 'is_staff')

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
