from django.urls import path
from .views import ActivityRateIssueView

urlpatterns = [
    path('<str:owner>/<str:repo>/', ActivityRateIssueView.as_view())
]
