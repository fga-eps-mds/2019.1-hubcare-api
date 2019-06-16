from django.urls import path
from commit_month.views import CommitMonthView

urlpatterns = [
    path('<str:owner>/<str:repo>/<str:token_auth>/',
         CommitMonthView.as_view()),
]
