from django.urls import path
from pull_request_template.views import PullRequestTemplateView


urlpatterns = [
    path(
        '<str:owner>/<str:repo>/',
        PullRequestTemplateView.as_view()
    ),
]
