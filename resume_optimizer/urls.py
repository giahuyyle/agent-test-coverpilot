from django.urls import path

from resume_optimizer.views import optimize_resume_view, optimize_resume_ui_view


urlpatterns = [
    path("optimize/", optimize_resume_view, name="optimize_resume"),
    path("optimize-ui/", optimize_resume_ui_view, name="optimize_resume_ui"),
]