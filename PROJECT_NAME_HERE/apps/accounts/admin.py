from django.contrib import admin
from .models import User
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'first_name', 'last_name', 'email', 'email_confirmed', 'is_active')
    list_filter = ('email_confirmed', 'is_active')
    search_fields = ('id', 'first_name', 'last_name', 'email')