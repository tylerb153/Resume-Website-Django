from django.shortcuts import render
import requests
from showcase.models import Project, Image

import datetime
import random

# Create your views here.
def home(request):
    # This updated and returns the featured project. it updates it if the date updated changes or there isn't one. it also checks if it's been accepted, unaccepted projects can't be featured. 
    featuredProject = updateFeaturedProject()

    # We are going to get the most recent project here for use in the recent project tile
    recentProject = Project.objects.filter(accepted=True).last()
    images = getRandomImages()

    mapLink = "https://dynmap.theminecraftcult.com/"
    
    context = {'recentProject': recentProject, 'featuredProject': featuredProject, 'images':images, 'mapLink': mapLink}
    return render(request, 'home.html', context=context)

def mapPage(request):
    dynmapLink = "https://dynmap.theminecraftcult.com/"
    bluemapLink = "https://bluemap.theminecraftcult.com/"
    dynmapLive = False
    bluemapLive = False
    try:
        if requests.head(dynmapLink, timeout=1).status_code == 200:
                dynmapLive = True
    except:
        pass
    try:
        if requests.get(bluemapLink, timeout=1, stream=True, headers={"Host": "bluemap.theminecraftcult.com", "User-Agent": "Mozilla/5.0"}).status_code < 400:
                bluemapLive = True
    except:
        pass
    
    queryString = request.META.get('QUERY_STRING', '')    

    return render(request, 'map.html', context={"dynmapLive": dynmapLive, "bluemapLive": bluemapLive, "dynmapLink": dynmapLink, "bluemapLink": bluemapLink, "queryString":queryString})

def aboutPage(request):
    return render(request, 'about.html')

def contactPage(request):
    return render(request, 'contact.html')

# Figure out if a new featured project needs to be selected in order to make sure it only change once per day
def updateFeaturedProject():
    global dateUpdated

    # Here we set up the globals if they don't have a value already
    try:
        if dateUpdated:
            pass
    except:
        dateUpdated = None

    featuredProjects = Project.objects.filter(featured=True)
    if dateUpdated != datetime.date.today() or len(featuredProjects) == 0:
        dateUpdated = datetime.date.today()
        if len(featuredProjects) > 0:
            for project in featuredProjects:
                project.featured = False
                project.save()

        projects = list(Project.objects.filter(accepted=True))
        if projects != []:    
            featuredProject = random.choice(projects)

            featuredProject.featured = True
            featuredProject.save()
            return featuredProject
        else:
            return None

    return featuredProjects.first()

def getRandomImages() -> list[Image]:
    projects = Project.objects.filter(accepted=True).prefetch_related('images')
    images = []
    for project in projects:
        images.extend(project.images.all())
    return random.sample(images, k=min(10, len(images)))

def getMapLink() -> str:
    try:
        if requests.head('https://map.tymler.com/', timeout=1).status_code == 200:
            mapLink = 'https://map.tymler.com/'
        elif requests.head('https://backupmap.tymler.com/', timeout=1).status_code == 200:
            mapLink = 'https://backupmap.tymler.com/'
        else:
            mapLink = "Offline"
    except:
        mapLink = "Offline"

    return mapLink