from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import models
from .models import MatatuGame
from decimal import Decimal
import json

@login_required
def game_lobby(request):
    """View to display available games and create new ones"""
    # Get all games waiting for a second player
    waiting_games = MatatuGame.objects.filter(status='waiting').exclude(player1=request.user)
    # Get user's active games
    my_games = MatatuGame.objects.filter(
        status__in=['waiting', 'active']
    ).filter(
        models.Q(player1=request.user) | models.Q(player2=request.user)
    )
    
    context = {
        'waiting_games': waiting_games,
        'my_games': my_games,
    }
    return render(request, 'matatu_game/lobby.html', context)

@login_required
def create_game(request):
    """Create a new game with a stake"""
    if request.method == 'POST':
        stake = request.POST.get('stake', 0)
        try:
            stake = Decimal(stake)
            if stake < 0:
                messages.error(request, "Stake must be a positive number")
                return redirect('matatu_game:lobby')
            
            game = MatatuGame.objects.create(
                player1=request.user,
                player1_stake=stake,
                status='waiting'
            )
            messages.success(request, f"Game created! Waiting for opponent to join with ${stake} stake")
            return redirect('matatu_game:game_detail', game_id=game.id)
        except ValueError:
            messages.error(request, "Invalid stake amount")
            return redirect('matatu_game:lobby')
    
    return redirect('matatu_game:lobby')

@login_required
def join_game(request, game_id):
    """Join an existing game"""
    game = get_object_or_404(MatatuGame, id=game_id)
    
    if game.status != 'waiting':
        messages.error(request, "This game is no longer available")
        return redirect('matatu_game:lobby')
    
    if game.player1 == request.user:
        messages.error(request, "You cannot join your own game")
        return redirect('matatu_game:lobby')
    
    if request.method == 'POST':
        stake = request.POST.get('stake', 0)
        try:
            stake = Decimal(stake)
            if stake != game.player1_stake:
                messages.error(request, f"You must stake ${game.player1_stake} to join this game")
                return redirect('matatu_game:lobby')
            
            game.player2 = request.user
            game.player2_stake = stake
            game.initialize_game()
            messages.success(request, f"Joined game! Total pot: ${game.get_total_pot()}")
            return redirect('matatu_game:game_detail', game_id=game.id)
        except ValueError:
            messages.error(request, "Invalid stake amount")
            return redirect('matatu_game:lobby')
    
    context = {'game': game}
    return render(request, 'matatu_game/join_game.html', context)

@login_required
def game_detail(request, game_id):
    """View for the actual game play"""
    game = get_object_or_404(MatatuGame, id=game_id)
    
    # Check if user is a player in this game
    if request.user not in [game.player1, game.player2]:
        messages.error(request, "You are not a player in this game")
        return redirect('matatu_game:lobby')
    
    # Determine which player the current user is
    is_player1 = request.user == game.player1
    
    # Get the appropriate hand for the current player
    if game.game_state:
        current_hand = game.game_state.get('player1_hand' if is_player1 else 'player2_hand', [])
        discard_pile = game.game_state.get('discard_pile', [])
        last_played = game.game_state.get('last_played')
    else:
        current_hand = []
        discard_pile = []
        last_played = None
    
    context = {
        'game': game,
        'is_player1': is_player1,
        'current_hand': current_hand,
        'hand_count': len(current_hand),
        'opponent_hand_count': len(game.game_state.get('player2_hand' if is_player1 else 'player1_hand', [])) if game.game_state else 0,
        'discard_pile': discard_pile,
        'last_played': last_played,
        'is_my_turn': game.current_turn == request.user,
        'total_pot': game.get_total_pot(),
    }
    return render(request, 'matatu_game/game_detail.html', context)

@login_required
def play_card(request, game_id):
    """Handle playing a card"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)
    
    game = get_object_or_404(MatatuGame, id=game_id)
    
    # Verify it's the player's turn
    if game.current_turn != request.user:
        return JsonResponse({'error': 'Not your turn'}, status=400)
    
    if game.status != 'active':
        return JsonResponse({'error': 'Game is not active'}, status=400)
    
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError) as e:
        return JsonResponse({'error': 'Invalid request data'}, status=400)
    
    card_index = data.get('card_index')
    if card_index is None:
        return JsonResponse({'error': 'card_index is required'}, status=400)
    
    try:
        card_index = int(card_index)
    except (ValueError, TypeError):
        return JsonResponse({'error': 'card_index must be an integer'}, status=400)
    
    # Determine which player
    is_player1 = request.user == game.player1
    hand_key = 'player1_hand' if is_player1 else 'player2_hand'
    
    # Get current hand
    hand = game.game_state.get(hand_key, [])
    
    if card_index < 0 or card_index >= len(hand):
        return JsonResponse({'error': 'Invalid card'}, status=400)
    
    # Play the card
    played_card = hand.pop(card_index)
    game.game_state['discard_pile'].append(played_card)
    game.game_state['last_played'] = played_card
    game.game_state[hand_key] = hand
    
    # Check if player won (no cards left)
    if len(hand) == 0:
        game.status = 'finished'
        game.winner = request.user
        game.save()
        return JsonResponse({
            'success': True,
            'game_over': True,
            'winner': request.user.username,
            'winnings': float(game.get_total_pot())
        })
    
    # Switch turns
    game.current_turn = game.player2 if is_player1 else game.player1
    game.save()
    
    return JsonResponse({
        'success': True,
        'game_over': False,
        'hand_count': len(hand)
    })

@login_required
def draw_card(request, game_id):
    """Handle drawing a card from the deck"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)
    
    game = get_object_or_404(MatatuGame, id=game_id)
    
    # Verify it's the player's turn
    if game.current_turn != request.user:
        return JsonResponse({'error': 'Not your turn'}, status=400)
    
    if game.status != 'active':
        return JsonResponse({'error': 'Game is not active'}, status=400)
    
    # Determine which player
    is_player1 = request.user == game.player1
    hand_key = 'player1_hand' if is_player1 else 'player2_hand'
    
    # Get draw pile
    draw_pile = game.game_state.get('draw_pile', [])
    
    if len(draw_pile) == 0:
        return JsonResponse({'error': 'No cards left to draw'}, status=400)
    
    # Draw a card
    drawn_card = draw_pile.pop(0)
    hand = game.game_state.get(hand_key, [])
    hand.append(drawn_card)
    
    game.game_state[hand_key] = hand
    game.game_state['draw_pile'] = draw_pile
    
    # Switch turns
    game.current_turn = game.player2 if is_player1 else game.player1
    game.save()
    
    return JsonResponse({
        'success': True,
        'hand_count': len(hand)
    })
