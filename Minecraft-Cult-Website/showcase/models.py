from django.db import models

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=100)

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
    thumbnail = models.ForeignKey('Image', on_delete=models.SET_NULL, null=True, related_name='Thumbnail')

    def delete(self, *args, **kwargs):
        if self.thumbnail:
            self.thumbnail.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title

def build_image_upload_path(instance, filename):
    if instance.build:
        return f'builds/{instance.build.id}/{filename}'
    else:
        return f'builds/static/{filename}'

class Image(models.Model):
    name = models.CharField(null=True, blank=True)
    build = models.ForeignKey(Build, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    image = models.ImageField(upload_to=build_image_upload_path)

    def save(self):
        if self.build and not self.name :
            self.name = self.build.title
        
        super().save()

    def __str__(self):
        return self.name

class BuildTag(models.Model):
    build = models.ForeignKey(Build, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT)
