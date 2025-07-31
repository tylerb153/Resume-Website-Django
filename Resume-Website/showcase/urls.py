from django.urls import path
from . import views

urlpatterns = [
    path("", views.showcase, name="showcase"),
    path("NewProject", views.createProject, name='createProject'),
    path("<slug:slug>", views.projectDetails, name='projectDetails'),
]