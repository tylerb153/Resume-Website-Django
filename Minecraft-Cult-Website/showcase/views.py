from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Build, Tag
from .forms import BuildForm

# Create your views here.
def showcase(request):
    searchQuery = request.GET.get('search', '')
    filter_string = request.GET.get('filters', '')

    filters = []
    for filter in filter_string.split(" "):
        if filter != "":
            filters.append(filter)
    print(filters)

    builds = Build.objects.filter(Q(title__icontains=searchQuery) | Q(creator__icontains=searchQuery) | Q(tags__name__icontains=searchQuery)).distinct()
    
    filter_query = Q()
    for filter in filters:
        filter_query |= Q(tags__name__iexact=filter)

    builds = builds.filter(filter_query).distinct()
    

    paginator = Paginator(builds, 12)
    page_number = request.GET.get('page')
    builds = paginator.get_page(page_number)
    
    tags = Tag.objects.all()
    context = {'tags': tags, 'builds': builds, 'searchQuery': searchQuery}
    return render(request, 'showcase.html', context)

def createBuild(request):
    if request.method == "POST":
        form = BuildForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('showcase')
    return render(request, 'showcase.html', {'form': form})