from django.urls import path
from contributors.views import DifferentsAuthorsView

urlpatterns = [
    path('different_authors/<str:owner>/<str:repo>/',
         DifferentsAuthorsView.as_view()),
]
