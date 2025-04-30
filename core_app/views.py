
from django.shortcuts import render
from jobs.models import Job
from Scholarships.models import Scholarship
from jobs.models import MemberOpportunity

from django.contrib.auth.decorators import login_required


def home_view(request):
    return render(request, 'home.html', {'user': request.user})
@login_required
def dashboard_view(request):
    jobs = Job.objects.all()
    scholarships = Scholarship.objects.all()
    opportunities = MemberOpportunity.objects.all()

    context = {
        'job_count': jobs.count(),
        'scholarship_count': scholarships.count(),
        'opportunity_count': opportunities.count(),
        'recent_opportunities': opportunities.order_by('-created_at')[:5],
    }
    return render(request, 'dashboard.html', context)
