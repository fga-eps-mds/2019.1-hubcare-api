from django.urls import path
from readme.views import ReadmeView


urlpatterns = [
    path(
        '<str:owner>/<str:repo>/<str:token_auth>/',
        ReadmeView.as_view()
    ),
]
