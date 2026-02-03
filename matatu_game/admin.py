from django.contrib import admin
from .models import MatatuGame

@admin.register(MatatuGame)
class MatatuGameAdmin(admin.ModelAdmin):
    list_display = ['id', 'player1', 'player2', 'status', 'player1_stake', 'player2_stake', 'winner', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['player1__username', 'player2__username']
    readonly_fields = ['created_at', 'updated_at']

