
from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView
from core import views as core_views
from leads import views as leads_views

urlpatterns = [
    
    # Redirects
    path('', RedirectView.as_view(url='/admin/'), name='home-redirect-admin'),
    path('api/', RedirectView.as_view(url='/admin/'), name='home-redirect-admin'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # Api endpoints
    path('api/login/', core_views.LoginView.as_view(), name='login'),
    path('api/profile/', core_views.ProfileView.as_view(), name='profile'),
    path('api/contact/', leads_views.ContactView.as_view(), name='contact'),
    path('api/quote/', leads_views.Quote.as_view(), name='contact'),
]
