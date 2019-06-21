from django.urls import path
from .views import ActivityRateIssueView

urlpatterns = [
    path('<str:owner>/<str:repo>/<str:token_auth>/',
         ActivityRateIssueView.as_view())
]
