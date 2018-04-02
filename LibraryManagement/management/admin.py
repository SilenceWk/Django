from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from management.models import *


class MyUserInline(admin.StackedInline):
    model = MyUser
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (MyUserInline,)


admin.site.site_header = '社团后台管理'
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Club)
