from django.shortcuts import render

# Create your views here.

from .models import AssociationHistory, ExecutiveMember, Constitution

def about_us(request):
    history = AssociationHistory.objects.first()
    members = ExecutiveMember.objects.all()
    constitution = Constitution.objects.first()

    return render(request, 'about/about_us.html', {
        'history': history,
        'members': members,
        'constitution': constitution
    })

