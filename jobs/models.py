from django.db import models

# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    application_link = models.URLField(blank=True)
    application_deadline = models.DateField()
    job_file = models.FileField(upload_to='job_descriptions/', blank=True, null=True)
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company}"

class Scholarship(models.Model):
    title = models.CharField(max_length=200)
    provider = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateField()
    application_link = models.URLField(blank=True)

    def __str__(self):
        return self.title
