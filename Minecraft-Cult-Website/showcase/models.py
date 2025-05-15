from django.db import models

# Create your models here.
class Build(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.CharField(max_length=100)
    tags = models.ManyToManyField('Tag', related_name='builds')
    # thumbnail = models.ForeignKey('Image', related_name='build', on_delete=models.PROTECT, null=False, blank=False)

    def __str__(self):
        return self.title


class Image(models.Model):
    buildID = models.ForeignKey(Build, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')


class Tag(models.Model):
    name = models.CharField(max_length=100)
