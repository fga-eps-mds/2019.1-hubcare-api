from django.urls import path
from .views import DifferentsAuthorsView
from django.urls import path, include

urlpatterns = [
    path('differentsauthors/<str:owner>/<str:repo>', DifferentsAuthorsView.as_view())
]