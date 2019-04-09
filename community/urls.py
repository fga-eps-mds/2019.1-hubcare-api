from django.urls import path
from .views import PullRequestTemplateView

urlpatterns = [
    path('pull_request_template/<str:owner>/<str:repo>', PullRequestTemplateView.as_view())
]