from django.urls import path
from . import views

urlpatterns = [
    path("", views.showcase, name="showcase"),
    path("NewBuild", views.createBuild, name='createBuild'),
    path("<slug:slug>", views.buildDetails, name='buildDetails'),
]