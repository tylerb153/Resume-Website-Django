from django.db import models
from django.conf import settings
import os
import shutil

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Build(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.CharField(max_length=100)
    coordsx = models.IntegerField(null=True, blank=True)
    coordsy = models.IntegerField(null=True, blank=True)
    coordsz = models.IntegerField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='builds', through='BuildTag')

    @property
    def thumbnail(self):
        return self.images.filter(thumbnail=True).first()

    def delete(self, *args, **kwargs):
        imageFolder = os.path.join(settings.MEDIA_ROOT, 'builds', str(self.id))
        super().delete(*args, **kwargs)
        if os.path.isdir(imageFolder):
            shutil.rmtree(imageFolder)
            

    def __str__(self):
        return self.title

def build_image_upload_path(instance, filename):
    if instance.build:
        return f'builds/{instance.build.id}/{filename}'
    else:
        return f'builds/static/{filename}'

class Image(models.Model):
    name = models.CharField(null=True, blank=True)
    build = models.ForeignKey(Build, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=build_image_upload_path)
    thumbnail = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class BuildTag(models.Model):
    build = models.ForeignKey(Build, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT)
