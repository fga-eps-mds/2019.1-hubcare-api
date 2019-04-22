from django.urls import path
from contribution_guide.views import ContributionGuideView


urlpatterns = [
    path(
        '<str:owner>/<str:repo>/',
        ContributionGuideView.as_view()
    ),
]
