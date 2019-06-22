from django.urls import path
from contributors.views import DifferentsAuthorsView

urlpatterns = [
    path('<str:owner>/<str:repo>/<str:token_auth>/',
         DifferentsAuthorsView.as_view()),
]
