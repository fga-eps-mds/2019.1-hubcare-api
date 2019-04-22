from django.urls import path
from license_metric.views import LicenseView


urlpatterns = [
    path(
        '<str:owner>/<str:repo>/',
        LicenseView.as_view()
    ),
]
