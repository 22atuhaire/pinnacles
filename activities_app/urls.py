from django.urls import path
from . import views

app_name = 'activities_app'
urlpatterns = [
    path('', views.activities_list, name='activities'),
]