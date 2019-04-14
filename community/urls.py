from django.urls import path
from .views import ReadmeView


urlpatterns = [
    path('readme/<str:owner>/<str:repo>/', ReadmeView.as_view()),
]
