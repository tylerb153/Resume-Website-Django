from django.shortcuts import render, redirect
from .models import Build, Tag
from .forms import BuildForm

# Create your views here.
def showcase(request):
    builds = Build.objects.all()
    tags = Tag.objects.all()
    context = {'tags': tags, 'builds': builds}
    return render(request, 'showcase.html', context)

def createBuild(request):
    if request.method == "POST":
        form = BuildForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('showcase')
    return render(request, 'showcase.html', {'form': form})