
# Create your models here.
from django.db import models

# Association History Model
class AssociationHistory(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title

# Executive Committee Member Model
class ExecutiveMember(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='executive_photos/')

    def __str__(self):
        return f"{self.name} - {self.position}"

# Constitution Document Model
class Constitution(models.Model):
    title = models.CharField(max_length=255)
    document = models.FileField(upload_to='constitutions/')

    def __str__(self):
        return self.title
