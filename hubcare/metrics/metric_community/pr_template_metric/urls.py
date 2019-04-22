from django.urls import path
from pr_template_metric.views import PullRequestTemplateView


urlpatterns = [
    path(
        '<str:owner>/<str:repo>/',
        PullRequestTemplateView.as_view()
    ),
]
