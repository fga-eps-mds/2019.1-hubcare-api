from django.urls import path
from issues.views.help_wanted_views import HelpWantedView

urlpatterns = [
    path('help_wanted/<str:owner>/<str:repo>/', HelpWantedView.as_view()),
]
