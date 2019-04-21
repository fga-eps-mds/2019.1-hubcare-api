from django.urls import path
from commits.views.contributors_views import DifferentsAuthorsView
from commits.views import CommitMonthView
from django.urls import path, include

urlpatterns = [

    path('differentsauthors/<str:owner>/<str:repo>',
         DifferentsAuthorsView.as_view()),
    path('commit_month/<str:owner>/<str:repo>/', CommitMonthView.as_view())
]
