from django.db import models
from Run.models import Run

# Create your models here.
class Album(models.Model):
    imgpath = models.ImageField()
    run = models.ForeignKey(Run, on_delete=models.CASCADE, blank = True, null=True)

    # def __str__(self):
    #     return self.id
 