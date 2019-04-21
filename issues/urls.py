from django.urls import path
from issues.views.help_wanted_views import HelpWantedView
from issues.views.good_first_issue_views import GoodFirstIssueView

url_gfi = 'good_first_issue/<str:owner>/<str:repo>/'

urlpatterns = [
    path('help_wanted/<str:owner>/<str:repo>/', HelpWantedView.as_view()),
    path(url_gfi, GoodFirstIssueView.as_view())
]
