from django.urls import path
from contribution_guide_metric.views import ContributionGuideView


urlpatterns = [
    path(
        '<str:owner>/<str:repo>/',
        ContributionGuideView.as_view()
    ),
]
