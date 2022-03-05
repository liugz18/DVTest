from django.db import models

# Create your models here.
class Sweep(models.Model):
    name = models.CharField(max_length=100, default="")

    # def __str__(self):
    #     return self.id
 