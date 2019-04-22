from django.urls import path
from help_wanted.views import HelpWantedView

urlpatterns = [
    path('<str:owner>/<str:repo>/', HelpWantedView.as_view()),
]
