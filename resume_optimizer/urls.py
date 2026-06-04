from django.urls import path

from resume_optimizer.views import optimize_resume_view


urlpatterns = [
    path("optimize/", optimize_resume_view, name="optimize_resume"),
]