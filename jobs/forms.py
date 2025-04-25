from django import forms
from .models import MemberOpportunity

class MemberOpportunityForm(forms.ModelForm):
    class Meta:
        model = MemberOpportunity
        fields = ['title', 'company', 'location', 'description', 'contact_email']
