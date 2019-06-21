from django.urls import path
from license.views import LicenseView


urlpatterns = [
    path(
        '<str:owner>/<str:repo>/<str:token_auth>/',
        LicenseView.as_view()
    ),
]
