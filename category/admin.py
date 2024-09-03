from django.contrib import admin
from .models import Category

# Register your models here.
# We want out model into admin panel
# To use it we need to register here

class CategoryAdmin(admin.ModelAdmin):
    # So here we need to make Prepopulated fields
    prepopulated_fields = {'slug':('category_name',)}
    # Also we need to make list display
    # These fields would be in the front of the Admin Category Panel
    list_display = ('category_name','slug')

admin.site.register(Category , CategoryAdmin)