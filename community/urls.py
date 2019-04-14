from django.urls import path
from community.views.license_view import LicenseView

urlpatterns = [
    path('license/<str:owner>/<str:repo>/', LicenseView.as_view()),
]
