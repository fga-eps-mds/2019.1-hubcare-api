from django.urls import path
from .views import LicenseView

urlpatterns = [
    path('license/<str:owner>/<str:repo>/', LicenseView.as_view() ),
]