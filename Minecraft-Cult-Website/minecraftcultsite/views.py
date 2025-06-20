from django.shortcuts import render
import requests
from showcase.models import Build, Image

import datetime
import random

# Create your views here.
def home(request):
    global featuredBuild
    
    updateFeaturedBuild()
    # We are going to get the most recent build here for use in the recent build tile
    recentBuild = Build.objects.filter(accepted=True).last()
    images = getRandomImages()
    
    context = {'recentBuild': recentBuild, 'featuredBuild': featuredBuild, 'images':images}
    return render(request, 'home.html', context=context)

def mapPage(request):
    try:
        if requests.head('https://map.tymler.com/', timeout=1).status_code == 200:
            map_link = 'https://map.tymler.com/'
        elif requests.head('https://backupmap.tymler.com/', timeout=1).status_code == 200:
            map_link = 'https://backupmap.tymler.com/'
        else:
            map_link = "Offline"
    except:
        map_link = "Offline"
    
    queryString = request.META.get('QUERY_STRING', '')    

    return render(request, 'map.html', context={"map_link": map_link, "queryString":queryString})


# Figure out if a new featured build needs to be selected in order to make sure it only change once per day
def updateFeaturedBuild():
    global featuredBuild
    global dateUpdated

    # Here we set up the globals if they don't have a value already
    try:
        if featuredBuild:
            pass
    except:
        featuredBuild = None

    try:
        if dateUpdated:
            pass
    except:
        dateUpdated = None


    if dateUpdated != datetime.date.today():
        dateUpdated = datetime.date.today()
        
        builds = list(Build.objects.filter(accepted=True))

        featuredBuild = random.choice(builds)

def getRandomImages() -> list[Image]:
    builds = Build.objects.filter(accepted=True).prefetch_related('images')
    images = []
    for build in builds:
        images.extend(build.images.all())
    print(images)
    return random.sample(images, k=min(10, len(images)))