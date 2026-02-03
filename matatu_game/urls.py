from django.urls import path
from . import views

app_name = 'matatu_game'

urlpatterns = [
    path('', views.game_lobby, name='lobby'),
    path('create/', views.create_game, name='create_game'),
    path('join/<int:game_id>/', views.join_game, name='join_game'),
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),
    path('game/<int:game_id>/play/', views.play_card, name='play_card'),
    path('game/<int:game_id>/draw/', views.draw_card, name='draw_card'),
]
