from django.urls import path
from community.views.contribution_guide_views import ContributionGuideView

urlpatterns = [
              path('contribution_guide/<str:owner>/<str:repo>/', ContributionGuideView.as_view())
              ]
