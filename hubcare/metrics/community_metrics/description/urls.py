from django.urls import path
from description.views import DescriptionView


urlpatterns = [
    path(
        '<str:owner>/<str:repo>/<str:token_auth>/',
        DescriptionView.as_view()
    ),
]
