from django.urls import path
from django.views.generic.base import RedirectView
from core.views import LoginView, ProfileView

urlpatterns = [
    # Redirects
    path('', RedirectView.as_view(url='/admin/'), name='home-redirect-admin'),
    path('api/', RedirectView.as_view(url='/admin/'), name='home-redirect-admin'),
    
    # Api endpoints
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/profile/', ProfileView.as_view(), name='profile'),
]