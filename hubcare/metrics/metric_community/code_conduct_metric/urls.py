from django.urls import path
from code_conduct_metric.views import CodeOfConductView


urlpatterns = [
    path(
        '<str:owner>/<str:repo>/',
        CodeOfConductView.as_view()
    )
]
