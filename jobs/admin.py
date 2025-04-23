from django.contrib import admin

# Register your models here
from .models import Job, Scholarship

admin.site.register(Job)
admin.site.register(Scholarship)
