from django.urls import path
from community.views.pr_template_view import PullRequestTemplateView
from community.views.license_view import LicenseView

urlpatterns = [
    path('pull_request_template/<str:owner>/<str:repo>',
         PullRequestTemplateView.as_view()),
    path('license/<str:owner>/<str:repo>/', LicenseView.as_view())
]
