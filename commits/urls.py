from django.urls import path
from commits.views import CommitYearView

urlpatterns = [
    path('commit_year/<str:owner>/<str:repo>/', CommitYearView.as_view()),
]