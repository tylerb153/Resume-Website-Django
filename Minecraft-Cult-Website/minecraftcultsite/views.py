from django.shortcuts import render, redirect
import requests

# Create your views here.
def home(request):
    return render(request, 'home.html')

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