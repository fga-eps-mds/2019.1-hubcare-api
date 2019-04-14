from django.urls import path
from community.views.issue_templates_views import IssueTemplatesView

urlpatterns = [
              path('issue_templates/<str:owner>/<str:repo>', IssueTemplatesView.as_view())
              ]