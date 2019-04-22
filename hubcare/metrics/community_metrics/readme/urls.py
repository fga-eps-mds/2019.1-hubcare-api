from django.urls import path
from readme.views import ReadmeView


urlpatterns = [
    path(
        '<str:owner>/<str:repo>/',
        ReadmeView.as_view()
    ),
]
