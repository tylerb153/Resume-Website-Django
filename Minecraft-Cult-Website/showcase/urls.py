from django.urls import path
from . import views

urlpatterns = [
    path("", views.showcase, name="showcase"),
    path("NewBuild", views.createBuild, name='createBuild'),
    # TODO: Change this int:id to be a slug
    path("<int:id>", views.buildDetails, name='buildDetails'),
]