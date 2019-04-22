from django.urls import path
from commit_week.views import CommitMonthView

urlpatterns = [
    path('commit_month/<str:owner>/<str:repo>/', CommitMonthView.as_view()),
]
