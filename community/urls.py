from django.urls import path
from .views import ReadmeView

urlpatterns = [
    #path('readme/', ReadmeView.as_view()),
    path('readme/<str:owner>/<str:repo>/', ReadmeView.as_view()),
]