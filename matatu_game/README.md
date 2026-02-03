# Matatu Card Game

A Django-based two-player card game where players can stake money and compete against each other.

## Features

- **Two-Player Gameplay**: Players can create or join games
- **Money Staking**: Each player must stake an equal amount to play
- **Turn-Based Gameplay**: Players take turns playing cards or drawing from the deck
- **Winner Takes All**: The first player to empty their hand wins the pot
- **Real-time Updates**: Game state updates automatically as players make moves

## How to Play

### Creating a Game

1. Navigate to the Matatu Game page from the main menu
2. Enter a stake amount (e.g., $10.00)
3. Click "Create Game"
4. Wait for an opponent to join

### Joining a Game

1. Navigate to the Matatu Game lobby
2. View available games waiting for players
3. Click "Join" on a game
4. Match the stake amount to join
5. Game starts automatically once both players are ready

### Playing the Game

- **Your Turn**: You can either play a card from your hand or draw a card from the deck
- **Objective**: Be the first player to empty your hand
- **Winner**: First player with no cards remaining wins the total pot (both stakes combined)

## Game Rules

1. Each player starts with 5 cards
2. Players take turns playing one card or drawing one card
3. The game continues until one player has no cards left
4. The winner receives the total pot (sum of both player stakes)

## Technical Details

### Models

- **MatatuGame**: Tracks game state, players, stakes, and winner
  - `player1`, `player2`: The two players in the game
  - `player1_stake`, `player2_stake`: Money staked by each player
  - `status`: Game status (waiting, active, finished)
  - `game_state`: JSON field storing deck, hands, and played cards
  - `winner`: The player who won the game

### URLs

- `/matatu/` - Game lobby
- `/matatu/create/` - Create a new game
- `/matatu/join/<game_id>/` - Join an existing game
- `/matatu/game/<game_id>/` - Play a game
- `/matatu/game/<game_id>/play/` - API endpoint to play a card
- `/matatu/game/<game_id>/draw/` - API endpoint to draw a card

## Installation

The Matatu game is already integrated into the Pinnacles project. To use it:

1. Make sure migrations are applied:
   ```bash
   python manage.py migrate matatu_game
   ```

2. Access the game through the main navigation menu

## Future Enhancements

- Add more complex Matatu rules (special cards, suits matching, etc.)
- Implement a tournament system
- Add game history and statistics
- Integrate with payment system for real money games
- Add spectator mode
- Implement chat between players
