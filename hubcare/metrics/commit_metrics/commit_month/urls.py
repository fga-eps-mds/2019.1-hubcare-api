from django.urls import path
from commit_month.views import CommitMonthView

urlpatterns = [
    path('<str:owner>/<str:repo>/', CommitMonthView.as_view()),
]
