from django.contrib import admin

# Register your models here
from .models import Job, MemberOpportunity

admin.site.register(Job)
# admin.site.register(Scholarship)
admin.site.register(MemberOpportunity)
