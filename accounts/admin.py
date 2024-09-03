from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class AccountAdmin(UserAdmin):
    # This listdisplay will do whatever fields we want to display in our Accounts Model of Admin Page
    # Since we are using Custom User Model , we can't directly do this , for this we need to follow some rules
    list_display = ('email','first_name','last_name','username','last_login','date_joined','is_active')
    list_display_links = ('email','first_name','last_name')
    readonly_fields = ('last_login','date_joined')
    # This -date_joined will show the users list in descending order
    ordering = ('-date_joined',)

    # So it makes Password Read only
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()



admin.site.register(Account , AccountAdmin)

# Note --> Before Migrating any changes , delete existing database for eg - db.sqlite3
# Bcox we don't require old data , as well as old super user
# Del. all the migrations from your Already existing Apps for eg - 
# [Category APP - migrations - 0001 , 0002.py ] 
