from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import Project, Tag, Image, ProjectTag
from .forms import ProjectForm

import random
import requests
import os
import json

# Create your views here.
def showcase(request):
    # Display the searched and filtered projects
    searchQuery = request.GET.get('search', '')
    filter_string = request.GET.get('filters', '')

    projects = Project.objects.filter(Q(title__icontains=searchQuery) | Q(creator__icontains=searchQuery) | Q(tags__name__icontains=searchQuery)).distinct()

    for filter in filter_string.split(","):
        if filter != "":
            projects = projects.filter(tags__name__iexact=filter)

    projects = projects.filter(accepted=True)

    paginator = Paginator(projects.order_by('orderNum'), 12)
    page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)
    
    tags = Tag.objects.filter(accepted=True)
    tags = list(tags.values_list("name", flat=True))

    context = {'tags': tags, 'projects': projects, }
    return render(request, 'showcase.html', context)

def createProject(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        tags = Tag.objects.all()
        try:
            if form.is_valid():
                try:
                    project = form.save()
                except Exception as e:
                    raise Exception(f"Creating Project Failed!\n{e}")

                #Process the images uploaded
                try:
                    thumbnail = request.FILES['thumbnail']
                    thumbnail = Image.objects.create(name=thumbnail.name , project=project, image=thumbnail, thumbnail=True)

                    images = request.FILES.getlist('images') 
                    for image in images:
                        Image.objects.create(name=image.name, project=project, image=image, thumbnail=False)
                except Exception as e:
                    raise Exception(f"Image Processing Failed!\n{e}")

                #Process the tags
                try:
                    if request.POST['tagsInput'] != "":
                        for tag in json.loads(request.POST['tagsInput']):
                            tagName = ""
                            for word in tag["value"].split():
                                tagName += word.capitalize() + " "
                            tagName = tagName.strip()
                            existingTag = tags.filter(name__iexact=tagName)
                            if existingTag:
                                ProjectTag.objects.create(tag=existingTag.first(), project=project)
                            else:
                                tag = Tag.objects.create(name=tagName)
                                ProjectTag.objects.create(tag=tag, project=project)
                except Exception as e:
                    raise Exception(f"Creating tags Failed!\n{e}")

                messages.success(request, 'Uploaded Project Successful! Please wait for approval.')
                
                try:
                    webhookURL = os.getenv('DISCORD_WEBHOOK_URL')
                    # print(request.project_absolute_uri(thumbnail.image.url))
                    discordJson = {
                        "content": f"{project.creator} just uploaded {project.title}",
                        "embeds": [
                            {
                                "image": {
                                    "url": request.project_absolute_uri(thumbnail.image.url)
                                },
                                "description": f"[Click here to review](http://192.168.254.10:8001/admin/showcase/project/)"
                            }
                        ]
                    }
                    response = requests.post(url=webhookURL, json=discordJson)
                    if response.status_code != 204:
                        raise Exception(f"Could not send webhook returned {response.status_code} {response.reason}")
                except Exception as e:
                    try:
                        discordJson = {
                            "content": f"{project.creator} just uploaded {project.title}",
                            "embeds": [
                                {
                                    "description": f"[Click here to review](http://192.168.254.10:8001/admin/showcase/project/)"
                                }
                            ]
                        }
                        requests.post(url=webhookURL, json=discordJson)
                        if response.status_code != 204:
                            raise Exception(f"Could not send webhook returned {response.status_code} {response.reason}")
                    except Exception as e:
                        print(f"Could not send webhook:\n{e}")            
            else:
                raise Exception("Form doesn't match!")
        except Exception as e:
            print(f"Error in project upload:\n{e}")
            messages.error(request, 'Upload Failed! Please refresh and try again', extra_tags='danger') 

    return redirect('showcase')

def projectDetails(request, slug):
    # Display the specific project
    if slug:
        projects = Project.objects.filter(accepted=True)
        project = projects.filter(Q(slug=slug)).first()

        projects = list(projects)
        projects.remove(project)
        while len(projects) >= 6:
            projects.remove(random.choice(projects))

        random.shuffle(projects)


        context = {'project': project, 'projects': projects}
        return render(request, 'projectDetails.html', context)
    