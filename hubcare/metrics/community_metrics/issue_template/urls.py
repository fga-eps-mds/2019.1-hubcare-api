from django.urls import path
from issue_template.views import IssueTemplateView


urlpatterns = [
    path(
        '<str:owner>/<str:repo>/<str:token_auth>/',
        IssueTemplateView.as_view()
    ),
]
