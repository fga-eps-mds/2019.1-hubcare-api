from django.urls import path
from description.views import DescriptionView


urlpatterns = [
    path(
        '<str:owner>/<str:repo>/',
        DescriptionView.as_view()
    ),
]
