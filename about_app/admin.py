from django.contrib import admin

from .models import AssociationHistory, ExecutiveMember, Constitution

admin.site.register(AssociationHistory)
admin.site.register(ExecutiveMember)
admin.site.register(Constitution)
