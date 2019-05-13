from django.urls import path
from commit_week.views import CommitMonthView

urlpatterns = [
    path('<str:owner>/<str:repo>/', CommitMonthView.as_view()),
]
