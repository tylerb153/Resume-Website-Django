from django.contrib import admin
from .models import Build, Tag, BuildTag, Image

class BuildTagInline(admin.TabularInline):
    model = BuildTag
    extra = 0

class ImageInline(admin.TabularInline):
    model = Image
    extra = 0

# Register your models here.
@admin.register(Build)
class BuildAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator']
    list_filter = ['creator', 'tags', ]
    search_fields = ['title', 'creator', 'tags']
    inlines = [BuildTagInline, ImageInline]



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    inlines = [BuildTagInline]

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['name', 'build', 'thumbnail']
    list_filter = ['build', 'thumbnail']
    search_fields = ['name', 'build']
