from django.urls import path
from license.views import LicenseView


urlpatterns = [
    path(
        '<str:owner>/<str:repo>/',
        LicenseView.as_view()
    ),
]
