from django.contrib.auth.decorators import login_required
from .forms import MemberOpportunityForm
from .models import MemberOpportunity
from django.shortcuts import render, redirect, get_object_or_404
from .models import Job
from .models import Scholarship
from django.contrib import messages

def job_list(request):
    jobs = Job.objects.order_by('-posted_on')
    return render(request, 'job_list.html', {'jobs': jobs})

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'job_detail.html', {'job': job})


def scholarship_list(request):
    scholarships = Scholarship.objects.all()
    return render(request, 'scholarship_list.html', {'scholarships': scholarships})

@login_required
def submit_opportunity(request):
    if request.method == 'POST':
        form = MemberOpportunityForm(request.POST)
        if form.is_valid():
            opportunity = form.save(commit=False)
            opportunity.created_by = request.user
            opportunity.save()
            messages.success(request, 'Your opportunity has been submitted successfully and is pending for review.')
            return redirect('jobs:member_opportunities')
    else:
        form = MemberOpportunityForm()
    return render(request, 'submit_opportunity.html', {'form': form})


def member_opportunities(request):
    opportunities = MemberOpportunity.objects.filter(is_approved=True).order_by('-created_at')
    return render(request, 'member_opportunities.html', {'opportunities': opportunities})
