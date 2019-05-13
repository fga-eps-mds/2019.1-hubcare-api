from django.urls import path
from contributors.views import DifferentsAuthorsView

urlpatterns = [
    path('<str:owner>/<str:repo>/',
         DifferentsAuthorsView.as_view()),
]
