from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import ContactForm
from showcase.models import Project, Image


import datetime
import random
import os
import requests

# Create your views here.
def home(request):
    # This updated and returns the featured project. it updates it if the date updated changes or there isn't one. it also checks if it's been accepted, unaccepted projects can't be featured. 
    featuredProject = updateFeaturedProject()

    # We are going to get the most recent project here for use in the recent project tile
    recentProject = Project.objects.filter(accepted=True).last()
    images = getRandomImages()
    
    context = {'recentProject': recentProject, 'featuredProject': featuredProject, 'images':images}
    return render(request, 'home.html', context=context)

def aboutPage(request):
    return render(request, 'about.html')

def contactPage(request):
    return render(request, 'contact.html')

def contactMessage(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        try:
            if form.is_valid():
                try:
                    webhookURL = os.getenv("DISCORD_WEBHOOK_URL")
                    json = {
                        "content": f"{form.cleaned_data["name"]} just sent the message:\n\t{form.cleaned_data["message"]}\n\nContact them back at [{form.cleaned_data["email"]}](mailto:{form.cleaned_data["email"]})",
                    }
                    response = requests.post(url=webhookURL, json=json)
                    if response.status_code != 204:
                        raise Exception(f"Could not send webhook returned {response.status_code} {response.reason}")
                    
                except Exception as e:
                    raise Exception(f'Error Sending Message in contactMessage:\n{e}')
                messages.success(request, 'Message successfully sent!')
        except Exception as e:
            print(f"Error in project upload:\n{e}")
            messages.error(request, 'Failed to send message! Please refresh and try again', extra_tags='danger')
    return redirect('contact')

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
