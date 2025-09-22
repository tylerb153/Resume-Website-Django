"""
URL configuration for minecraftcultsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import include, path
from . import views

from django.views.generic import RedirectView

from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('home/', RedirectView.as_view(url='/', permanent=True)),
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('projects/', include('showcase.urls')),
    # path('about/', views.aboutPage, name='about'),
    path('contact/', views.contactPage, name='contact'),
    path('contactMessage', views.contactMessage, name='contactMessage'),
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT})
]# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
