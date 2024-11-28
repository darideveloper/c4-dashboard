
from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView
from core.views import LoginView, ProfileView
from leads.views import ContactView

urlpatterns = [
    
    # Redirects
    path('', RedirectView.as_view(url='/admin/'), name='home-redirect-admin'),
    path('api/', RedirectView.as_view(url='/admin/'), name='home-redirect-admin'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # Api endpoints
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/profile/', ProfileView.as_view(), name='profile'),
    path('api/contact/', ContactView.as_view(), name='contact'),
]
