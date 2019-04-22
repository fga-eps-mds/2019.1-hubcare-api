"""community_metrics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('code_of_conduct/', include('code_conduct_metric.urls')),
    path('contribution_guide/', include('contribution_guide_metric.urls')),
    path('issue_template/', include('issue_template_metric.urls')),
    path('license/', include('license_metric.urls')),
    path('pull_request_template/', include('pr_template_metric.urls')),
    path('release_note/', include('release_note.urls')),
    path('readme/', include('readme.urls')),
    path('description/', include('description.urls')),
]
