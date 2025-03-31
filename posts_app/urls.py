from django.urls import path
from . import views

app_name = 'news'
# The 'app_name' variable is used to create namespaced URLs for the app.
urlpatterns = [
    path('', views.news_list_view, name='news_list'),
]

