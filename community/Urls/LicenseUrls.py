from django.urls import path
from community.Views.LicenseView import LicenseView

urlpatterns = [
    path('license/<str:owner>/<str:repo>/', LicenseView.as_view() ),
]