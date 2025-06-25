from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
import shutil

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    accepted = models.BooleanField(default=False)

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
    slug = models.SlugField(unique=True, blank=True)

    accepted = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)

    @property
    def thumbnail(self):
        return self.images.filter(thumbnail=True).first()

    def generateSlug(self, title: str):
        slug = slugify(title)
        uniqueSlug = slug
        counter = 1

        while len(self.__class__.objects.filter(slug__iexact=uniqueSlug)) > 0:
            uniqueSlug = f'{slug}-{counter}'
            counter += 1
        
        return uniqueSlug
            
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generateSlug(self.title)
        super().save(*args, **kwargs)
        

    def __str__(self):
        return self.title
    
@receiver(post_delete, sender=Build)
def deleteBuildFiles(sender, instance, **kwargs):
    imageFolder = os.path.join(settings.MEDIA_ROOT, 'builds', str(instance.id))
    if os.path.isdir(imageFolder):
        shutil.rmtree(imageFolder)

def getImageUploadPath(instance, filename):
    if instance.build:
        return f'builds/{instance.build.id}/{filename}'
    else:
        return f'builds/media/{filename}'

class Image(models.Model):
    name = models.CharField(null=True, blank=True)
    build = models.ForeignKey(Build, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=getImageUploadPath)
    thumbnail = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
@receiver(post_delete, sender=Image)
def deleteImageFile(sender, instance, **kwargs):
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)

class BuildTag(models.Model):
    build = models.ForeignKey(Build, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
