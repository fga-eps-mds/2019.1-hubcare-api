from django.urls import path
from .views import PullRequestTemplateView

urlpatterns = [
    path('pull_requests/<str:owner>/<str:repo>', PullRequestTemplateView.as_view() ),
]