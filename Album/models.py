from django.db import models

# Create your models here.


# Create your models here.
class Album(models.Model):
    imgpath = models.CharField(max_length=64)
    run = models.ForeignKey(to="Run.Run", on_delete=models.CASCADE)

    def __str__(self):
        return self.book_name
