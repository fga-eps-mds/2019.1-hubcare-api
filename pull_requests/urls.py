from django.urls import path
from .views import PullRequestTemplateView

urlpatterns = [
    path('pull_requests/', PullRequestTemplateView.as_view() ),
]
