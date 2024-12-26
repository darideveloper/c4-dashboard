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
    list_filter = ['status', 'added_on', 'updated_on']
    list_per_page = 50
    
    
@admin.register(models.CompanySector)
class CompanySectorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_per_page = 50
    ordering = ['name']
    

@admin.register(models.CompanyEmployees)
class CompanyEmployeesAdmin(admin.ModelAdmin):
    list_display = ['key']
    search_fields = ['key']
    list_per_page = 50
    ordering = ['id']
    

@admin.register(models.Features)
class FeaturesAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_per_page = 50
    ordering = ['name']
    

@admin.register(models.ResidentialType)
class ResidentialTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_per_page = 50
    ordering = ['name']
    
    
@admin.register(models.QuoteCompany)
class QuoteCompanyAdmin(admin.ModelAdmin):
    list_display = [
        'contact',
        'status',
        'sector',
        'added_on',
        'updated_on'
    ]
    search_fields = [
        'contact__name',
        'contact__address',
        'contact__email',
        'contact__phone',
        'status__name',
        'sector__name',
        'employees__key',
        'features__name',
        'added_on',
        'updated_on'
    ]
    list_per_page = 20
    list_filter = ['status', 'sector', 'employees', 'features']
    ordering = ['-added_on']
    

@admin.register(models.MonitoringUser)
class MonitoringUserAdmin(admin.ModelAdmin):
    list_display = ['name', 'key']
    search_fields = ['name', 'key']
    list_per_page = 50
    ordering = ['name']
    
@admin.register(models.MonitoringTarget)
class MonitoringTargetAdmin(admin.ModelAdmin):
    list_display = ['name', 'key']
    search_fields = ['name', 'key']
    list_per_page = 50
    ordering = ['name']

@admin.register(models.QuoteResidential)
class QuoteResidentialAdmin(admin.ModelAdmin):
    list_display = [
        'contact',
        'status',
        'type',
        'added_on',
        'updated_on'
    ]
    search_fields = [
        'contact__name',
        'contact__address',
        'contact__email',
        'contact__phone',
        'status__name',
        'type__name',
        'features__name',
        'added_on',
        'updated_on'
    ]
    list_per_page = 20
    list_filter = ['status', 'type', 'features']
    ordering = ['-added_on']