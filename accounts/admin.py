from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CodehubUser
from django.contrib.auth.models import Group


UserAdmin.list_display = ('id','username','email','is_staff')
UserAdmin.list_filter = ('id','username','email','is_staff')
admin.site.register(CodehubUser, UserAdmin)
admin.site.unregister(Group)