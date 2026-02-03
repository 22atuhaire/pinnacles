

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core_app.urls')),
    path('login/', include('auth_app.urls')),
    path('logout/', include('auth_app.urls')),
    path('register/', include('auth_app.urls')),
    path('news/', include('posts_app.urls')),
    path('activities/', include('activities_app.urls')),
    path('members/', include('members_app.urls')),
    path('about_us/', include('about_app.urls')),
    path('jobs/', include('jobs.urls')),
    path('scholarships/', include('Scholarships.urls')),
    path('matatu/', include('matatu_game.urls')),

] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


