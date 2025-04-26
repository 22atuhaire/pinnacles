from django.db import models

# Create your models here.
class Scholarship(models.Model):
    title = models.CharField(max_length=200)
    provider = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateField()
    application_link = models.URLField(blank=True)

    def __str__(self):
        return self.title
    