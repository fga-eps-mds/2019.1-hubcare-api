from django.urls import path
from .views import ReadmeView
from community.views.release_note_view import ReleaseNoteCheckView


urlpatterns = [
    path('<str:owner>/<str:repo>/',
         ReleaseNoteCheckView.as_view()),
]
