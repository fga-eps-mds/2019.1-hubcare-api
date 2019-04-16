from django.urls import path
from community.views.contribution_guide_views import ContributionGuideView

aux = 'contribution_guide/<str:owner>/<str:repo>/'
urlpatterns = [
    path(aux, ContributionGuideView.as_view())
]
