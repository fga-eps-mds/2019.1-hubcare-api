from django.urls import path
from .views import PullRequestQualityView

urlpatterns = [
    path('<str:owner>/<str:repo>/<str:token_auth>/', PullRequestQualityView.as_view())
]
