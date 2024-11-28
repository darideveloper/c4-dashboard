from django.contrib import admin
from leads import models


@admin.register(models.Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_per_page = 50
    

@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'status', 'phone',
                    'address', 'added_on', 'updated_on']
    search_fields = ['name', 'email', 'status__name', 'phone', 'address']
    list_filter = ['status']
    list_per_page = 50