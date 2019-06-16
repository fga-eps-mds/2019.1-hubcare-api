from django.urls import path
from release_note.views import ReleaseNoteView


urlpatterns = [
    path(
        '<str:owner>/<str:repo>/<str:token_auth>/',
        ReleaseNoteView.as_view()
    ),
]
