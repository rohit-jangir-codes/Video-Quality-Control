from django.db import models

class Video(models.Model):
    filename = models.CharField(max_length=255)
    path = models.CharField(max_length=255)

    def __str__(self):
        return self.filename
