
# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Job
from .models import Scholarship

def job_list(request):
    jobs = Job.objects.order_by('-posted_on')
    return render(request, 'job_list.html', {'jobs': jobs})

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'job_detail.html', {'job': job})


def scholarship_list(request):
    scholarships = Scholarship.objects.all()
    return render(request, 'scholarship_list.html', {'scholarships': scholarships})
