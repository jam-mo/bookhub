from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ('email', 'username','fullname','first_name','last_name','status')
    search_fields = ('email', 'username','fullname', 'first_name', 'last_name','status')


    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(CustomUser, AccountAdmin)