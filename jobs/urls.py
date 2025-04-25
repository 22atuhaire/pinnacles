from django.urls import path
from . import views

app_name = 'jobs'
urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
    path('scholarships/', views.scholarship_list, name='scholarship_list'),
    path('member-opportunities/', views.member_opportunities, name='member_opportunities'),
    path('submit-opportunity/', views.submit_opportunity, name='submit_opportunity'),
]
