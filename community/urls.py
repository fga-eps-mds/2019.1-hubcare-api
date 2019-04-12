from django.urls import path
from community.views.pr_template_view import PullRequestTemplateView

urlpatterns = [
               path('pull_request_template/<str:owner>/<str:repo>',
                    PullRequestTemplateView.as_view())
               ]
