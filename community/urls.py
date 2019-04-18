from django.urls import path
from .views import ReadmeView
from community.views.contribution_guide_views import ContributionGuideView
from community.views.issue_templates_views import IssueTemplatesView
from community.views.pr_template_view import PullRequestTemplateView
from community.views.license_view import LicenseView


url_issue = 'issue_templates/<str:owner>/<str:repo>/'
aux = 'contribution_guide/<str:owner>/<str:repo>/'

urlpatterns = [
    path(url_issue, IssueTemplatesView.as_view()),
    path('pull_request_template/<str:owner>/<str:repo>',
         PullRequestTemplateView.as_view()),
    path('license/<str:owner>/<str:repo>/', LicenseView.as_view()),
    path('readme/<str:owner>/<str:repo>/', ReadmeView.as_view()),
    path(aux, ContributionGuideView.as_view())
]
