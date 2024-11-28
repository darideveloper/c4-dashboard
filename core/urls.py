from django.urls import path
from django.views.generic.base import RedirectView

urlpatterns = [
    # Redirect from 'old-url/' to 'new-url/'
    path('', RedirectView.as_view(url='/admin/'), name='home-redirect-admin'),
]