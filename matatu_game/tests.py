from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from .models import MatatuGame

class MatatuGameTestCase(TestCase):
    def setUp(self):
        """Set up test users and client"""
        self.client = Client()
        self.user1 = User.objects.create_user(username='testplayer1', password='testpass123')
        self.user2 = User.objects.create_user(username='testplayer2', password='testpass123')
    
    def test_create_game(self):
        """Test creating a new game"""
        self.client.login(username='testplayer1', password='testpass123')
        response = self.client.post(reverse('matatu_game:create_game'), {'stake': '10.00'})
        
        # Should redirect after creation
        self.assertEqual(response.status_code, 302)
        
        # Check game was created
        game = MatatuGame.objects.first()
        self.assertIsNotNone(game)
        self.assertEqual(game.player1, self.user1)
        self.assertEqual(game.player1_stake, Decimal('10.00'))
        self.assertEqual(game.status, 'waiting')
    
    def test_join_game(self):
        """Test joining an existing game"""
        # Create a game with user1
        game = MatatuGame.objects.create(player1=self.user1, player1_stake=Decimal('10.00'))
        
        # User2 joins the game
        self.client.login(username='testplayer2', password='testpass123')
        response = self.client.post(
            reverse('matatu_game:join_game', args=[game.id]),
            {'stake': '10.00'}
        )
        
        # Should redirect after joining
        self.assertEqual(response.status_code, 302)
        
        # Check game was updated
        game.refresh_from_db()
        self.assertEqual(game.player2, self.user2)
        self.assertEqual(game.player2_stake, Decimal('10.00'))
        self.assertEqual(game.status, 'active')
        self.assertEqual(game.get_total_pot(), Decimal('20.00'))
    
    def test_game_initialization(self):
        """Test that game initializes properly"""
        game = MatatuGame.objects.create(
            player1=self.user1,
            player2=self.user2,
            player1_stake=Decimal('10.00'),
            player2_stake=Decimal('10.00')
        )
        game.initialize_game()
        
        # Check game state
        self.assertIsNotNone(game.game_state)
        self.assertEqual(len(game.game_state['player1_hand']), 5)
        self.assertEqual(len(game.game_state['player2_hand']), 5)
        self.assertGreater(len(game.game_state['draw_pile']), 0)
        self.assertEqual(game.status, 'active')
        self.assertEqual(game.current_turn, self.user1)
    
    def test_lobby_view_requires_login(self):
        """Test that lobby requires authentication"""
        response = self.client.get(reverse('matatu_game:lobby'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_lobby_view_authenticated(self):
        """Test that authenticated users can access lobby"""
        self.client.login(username='testplayer1', password='testpass123')
        response = self.client.get(reverse('matatu_game:lobby'))
        self.assertEqual(response.status_code, 200)

