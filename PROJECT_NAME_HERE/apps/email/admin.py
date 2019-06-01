from django.contrib import admin
from .models import Email, EmailQueue

# Register your models here.
@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('from_email', 'to_email', 'subject', 'html_text', 'plain_text', 'created_on', 'modified_on')

@admin.register(EmailQueue)
class EmailQueueAdmin(admin.ModelAdmin):
    list_display = ('email', 'status', 'status_msg', 'created_on', 'modified_on')
