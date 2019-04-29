from django.urls import path
from release_note.views import ReleaseNoteCheckView


urlpatterns = [
    path(
        '<str:owner>/<str:repo>/',
        ReleaseNoteCheckView.as_view()
    ),
]
