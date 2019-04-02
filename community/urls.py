from django.urls import path
from .views import LicenseView

urlpatterns = [
    path('license', LicenseView.as_view() ),
]