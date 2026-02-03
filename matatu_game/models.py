from django.db import models
from django.contrib.auth.models import User
import random
import json

class MatatuGame(models.Model):
    """Represents a game session between two players"""
    STATUS_CHOICES = [
        ('waiting', 'Waiting for Players'),
        ('active', 'Active'),
        ('finished', 'Finished'),
    ]
    
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matatu_games_as_player1')
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matatu_games_as_player2', null=True, blank=True)
    player1_stake = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    player2_stake = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    current_turn = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_turn_games')
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_games')
    game_state = models.JSONField(default=dict, blank=True)  # Store deck, hands, played cards, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Game {self.id}: {self.player1.username} vs {self.player2.username if self.player2 else 'Waiting'}"
    
    def initialize_game(self):
        """Initialize the game deck and deal cards"""
        # Create a standard 52-card deck
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        deck = [{'suit': suit, 'rank': rank} for suit in suits for rank in ranks]
        random.shuffle(deck)
        
        # Deal 5 cards to each player
        player1_hand = deck[:5]
        player2_hand = deck[5:10]
        draw_pile = deck[10:]
        
        # First card on discard pile
        discard_pile = []
        
        self.game_state = {
            'player1_hand': player1_hand,
            'player2_hand': player2_hand,
            'draw_pile': draw_pile,
            'discard_pile': discard_pile,
            'last_played': None,
        }
        self.current_turn = self.player1
        self.status = 'active'
        self.save()
    
    def get_total_pot(self):
        """Calculate total pot for the winner"""
        return self.player1_stake + self.player2_stake
    
    class Meta:
        ordering = ['-created_at']
