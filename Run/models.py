from django.db import models

# Create your models here.
# Create your models here.
class Run(models.Model):
    popsize = models.DecimalField(max_digits=19, decimal_places=10, default=0)
    density = models.FloatField(default=0)
    fips = models.DecimalField(max_digits=8, decimal_places=1, default=0)
    startdate = models.CharField(max_length=100, default="")
    finishdate = models.CharField(max_length=100, default="")
    key = models.CharField(max_length=100, default="")
    user = models.CharField(max_length=100, default="")
    where = models.CharField(max_length=100, default="")
    

    def __str__(self):
        return self.key
