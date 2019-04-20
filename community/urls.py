from django.urls import path
from .views import ReadmeView
from community.views.code_of_conduct_views import CodeOfConductView
from community.views.contribution_guide_views import ContributionGuideView
from community.views.issue_templates_views import IssueTemplatesView
from community.views.pr_template_view import PullRequestTemplateView
from community.views.license_view import LicenseView
from community.views.release_note_view import ReleaseNoteCheckView
from community.views.repository_description_view \
    import DescriptionView


aux = 'contribution_guide/<str:owner>/<str:repo>/'
url_issue = 'issue_templates/<str:owner>/<str:repo>/'
url_code_of_conduct = 'code_of_conduct/<str:owner>/<str:repo>/'

urlpatterns = [
    path(url_code_of_conduct, CodeOfConductView.as_view()),
    path(url_issue, IssueTemplatesView.as_view()),
    path('pull_request_template/<str:owner>/<str:repo>/',
         PullRequestTemplateView.as_view()),
    path('license/<str:owner>/<str:repo>/', LicenseView.as_view()),
    path('readme/<str:owner>/<str:repo>/', ReadmeView.as_view()),
    path(aux, ContributionGuideView.as_view()),
    path('realeasenotecheck/<str:owner>/<str:repo>/',
         ReleaseNoteCheckView.as_view()),
    path('description/<str:owner>/<str:repo>/',
         DescriptionView.as_view())
]
