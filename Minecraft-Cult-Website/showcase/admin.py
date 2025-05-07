from django.contrib import admin
from .models import Build, Tag

# Register your models here.
@admin.register(Build)
class BuildAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator']
    list_filter = ['creator', 'tags', ]
    search_fields = ['title', 'creator', 'tags']



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']