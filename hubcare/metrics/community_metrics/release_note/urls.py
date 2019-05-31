from django.urls import path
from release_note.views import ReleaseNoteView


urlpatterns = [
    path(
        '<str:owner>/<str:repo>/',
        ReleaseNoteView.as_view()
    ),
]
