from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django_resized import ResizedImageField
import os
import shutil

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag, related_name='projects', through='ProjectTag')
    slug = models.SlugField(unique=True, blank=True)

    accepted = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    recent = models.BooleanField(default=False)

    orderNum = models.IntegerField(default=1)

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
    
@receiver(post_delete, sender=Project)
def deleteProjectFiles(sender, instance, **kwargs):
    imageFolder = os.path.join(settings.MEDIA_ROOT, 'projects', str(instance.id))
    if os.path.isdir(imageFolder):
        shutil.rmtree(imageFolder)

def getImageUploadPath(instance, filename):
    if instance.project:
        return f'projects/{instance.project.id}/{filename}'
    else:
        return f'projects/media/{filename}'

class Image(models.Model):
    name = models.CharField(null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = ResizedImageField(force_format="WEBP", size=None, upload_to=getImageUploadPath)
    thumbnail = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
@receiver(post_delete, sender=Image)
def deleteImageFile(sender, instance, **kwargs):
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)

class ProjectTag(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
