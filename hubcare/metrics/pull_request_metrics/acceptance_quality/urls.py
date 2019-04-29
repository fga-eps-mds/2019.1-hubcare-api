from django.urls import path
from .views import PullRequestQualityView

urlpatterns = [
    path('<str:owner>/<str:repo>/', PullRequestQualityView.as_view())
]
