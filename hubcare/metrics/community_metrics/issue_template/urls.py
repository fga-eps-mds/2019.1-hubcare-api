from django.urls import path
from issue_template.views import IssueTemplateView


urlpatterns = [
    path(
        '<str:owner>/<str:repo>/',
        IssueTemplateView.as_view()
    ),
]
