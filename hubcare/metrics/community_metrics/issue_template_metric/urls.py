from django.urls import path
from issue_template_metric.views import IssueTemplatesView


urlpatterns = [
    path(
        '<str:owner>/<str:repo>/',
        IssueTemplatesView.as_view()
    ),
]
