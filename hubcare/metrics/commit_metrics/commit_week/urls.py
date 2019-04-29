from django.urls import path
from commit_week.views import CommitMonthView

urlpatterns = [
    path('commit_week/<str:owner>/<str:repo>/', CommitMonthView.as_view()),
]
