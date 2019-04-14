from django.urls import path
from commits.views import CommitMonthView

urlpatterns = [
    path('commit_month/<str:owner>/<str:repo>/', CommitMonthView.as_view()),
]