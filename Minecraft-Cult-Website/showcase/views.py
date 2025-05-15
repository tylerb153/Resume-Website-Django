from django.shortcuts import render
from .models import Build, Tag

# Create your views here.
def showcase(request):
    builds = Build.objects.all()
    tags = Tag.objects.all()
    context = {'tags': tags, 'builds': builds}
    return render(request, 'showcase.html', context)