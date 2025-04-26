from django.shortcuts import render
from.models import Scholarship

# Create your views here.

def scholarship_list(request):
    scholarships = Scholarship.objects.all()
    return render(request, 'scholarship_list.html', {'scholarships': scholarships})