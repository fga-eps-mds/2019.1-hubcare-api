from django.urls import path
from community.views.issue_templates_views import IssueTemplatesView
from community.views.pr_template_view import PullRequestTemplateView
from community.views.license_view import LicenseView

url_issue = 'issue_templates/<str:owner>/<str:repo>/'
urlpatterns = [
    path(url_issue, IssueTemplatesView.as_view()),
    path('pull_request_template/<str:owner>/<str:repo>',
         PullRequestTemplateView.as_view()),
    path('license/<str:owner>/<str:repo>/', LicenseView.as_view())
]
