from django.urls import path
from .views import PullRequestTemplateView

urlpatterns = [
    path('pull_requests/<str:owner>/<str:repo>/contents/.github/', PullRequestTemplateView.as_view() ),
]