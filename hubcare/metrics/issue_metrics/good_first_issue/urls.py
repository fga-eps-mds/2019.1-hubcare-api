from django.urls import path
# from good_first_issue.views import HelpWantedView
from good_first_issue.views import GoodFirstIssueView

urlpatterns = [
    path('<str:owner>/<str:repo>/', GoodFirstIssueView.as_view()),
]
