import random
from copy import deepcopy

class MonteCarloBot:
    def __init__(self, num_simulations=100):
        self.num_simulations = num_simulations

    def choose_move(self, player_hand, card_in_middle, opponent_hand_size, deck_size, is_initiative):
        """
        Choose the best move based on Monte Carlo simulation results.
        
        Args:
            player_hand: List of cards in bot's hand
            card_in_middle: Current card in the middle (or None if no card)
            opponent_hand_size: Number of cards in opponent's hand
            deck_size: Number of remaining cards in deck
            is_initiative: Boolean indicating if bot has initiative
        
        Returns:
            (card_index, should_pass): Tuple of chosen card index and whether to pass
        """
        if not player_hand:
            return None, True

        # If we're not initiative and there's no card in middle, play anything
        if not is_initiative and not card_in_middle:
            return 0, False

        # Initialize scores for each possible move
        move_scores = {i: 0 for i in range(len(player_hand))}
        pass_score = 0

        # Run simulations for each possible move
        for _ in range(self.num_simulations):
            # Try each possible move
            for i, card in enumerate(player_hand):
                if self._is_playable(card, card_in_middle, is_initiative):
                    # Simulate game after playing this card
                    score = self._simulate_game(
                        player_hand[:i] + player_hand[i+1:],
                        [card] if not card_in_middle else card_in_middle + [card],
                        opponent_hand_size,
                        deck_size,
                        is_initiative
                    )
                    move_scores[i] += score

            # Simulate passing if we have initiative and there's a card in middle
            if is_initiative and card_in_middle:
                pass_score += self._simulate_game(
                    player_hand,
                    card_in_middle,
                    opponent_hand_size,
                    deck_size,
                    is_initiative,
                    passed=True
                )

        # Find best move
        best_move_score = max(move_scores.values(), default=-float('inf'))
        pass_score = pass_score / self.num_simulations if is_initiative and card_in_middle else -float('inf')

        # If passing is better than playing any card
        if pass_score > best_move_score:
            return None, True

        # Find the best card to play
        best_moves = [i for i, score in move_scores.items() 
                     if score == best_move_score and 
                     self._is_playable(player_hand[i], card_in_middle, is_initiative)]
        
        if best_moves:
            return random.choice(best_moves), False
        return None, True

    def _is_playable(self, card, card_in_middle, is_initiative):
        """Check if a card is playable in the current state."""
        if not card_in_middle:
            return True
        if not is_initiative:
            return True
        if card.rank == "7":
            return True
        if card.rank == card_in_middle[0].rank:
            return True
        return False

    def _simulate_game(self, player_hand, middle_cards, opponent_hand_size, deck_size, is_initiative, passed=False):
        """
        Simulate a random game continuation from the current state.
        Returns a score representing how good this continuation is for the bot.
        """
        # If we passed, opponent gets the points
        if passed:
            return -sum(card.get_score() for card in middle_cards)

        # If opponent has no cards, they can't respond and we win
        if opponent_hand_size == 0:
            return sum(card.get_score() for card in middle_cards)

        # Simulate opponent's random move
        if random.random() < 0.7:  # 70% chance opponent has a valid response
            # Opponent continues the exchange
            return -self._simulate_game(
                player_hand,
                middle_cards,
                opponent_hand_size - 1,
                deck_size,
                not is_initiative
            )
        else:
            # Opponent can't respond, we win the exchange
            return sum(card.get_score() for card in middle_cards)