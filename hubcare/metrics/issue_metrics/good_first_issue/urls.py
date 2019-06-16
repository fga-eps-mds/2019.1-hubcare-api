from django.urls import path
# from good_first_issue.views import HelpWantedView
from good_first_issue.views import GoodFirstIssueView

urlpatterns = [
    path('<str:owner>/<str:repo>/<str:token_auth>/',
         GoodFirstIssueView.as_view()),
]
