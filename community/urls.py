from django.urls import path
from community.views.issue_templates_views import IssueTemplatesView

aux = 'issue_templates/<str:owner>/<str:repo>/'
urlpatterns = [
    path(aux, IssueTemplatesView.as_view())
]
