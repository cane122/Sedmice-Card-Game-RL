import random
from copy import deepcopy

class MonteCarloBot:
    def __init__(self, num_simulations=100):
        self.num_simulations = num_simulations

    def choose_move(self, player_hand, card_in_middle, cards_in_the_deck, opponent_hand_size, is_initiative):
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
                    strategic_penalty = self._calculate_penalty(card)
                    score = self._simulate_game(
                        player_hand[:i] + player_hand[i+1:],
                        [card] if not card_in_middle else card_in_middle + [card],
                        cards_in_the_deck,
                        opponent_hand_size,
                        is_initiative
                    )
                    move_scores[i] += score - strategic_penalty

            # Simulate passing if we have initiative and there's a card in middle
            if is_initiative and card_in_middle:
                pass_score += self._simulate_game(
                    player_hand,
                    card_in_middle,
                    cards_in_the_deck,
                    opponent_hand_size,
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
    
    def _calculate_penalty(self, card):
        if card.rank == "7":
            return 10 
        return 0
    
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

    def _simulate_game(self, player_hand, middle_cards, cards_in_the_deck, opponent_hand_size, is_initiative, passed=False):
        """
        Simulate a continuation of the game, tracking whose turn it is.
        Returns a score based on the outcome of this simulated continuation.
        
        Args:
            player_hand (list): List of cards in bot's hand
            middle_cards (list): Cards currently in the middle (e.g., cards played so far)
            cards_in_the_deck (list): cards currently unknown to the bot
            opponent_hand_size (int): Number of cards in the opponent's hand
            is_initiative (bool): Whether it's the bot's turn to play
            passed (bool): Whether the bot decides to pass
        
        Returns:
            score (int): A score representing how favorable the game state is for the bot
        """
        # If the bot passed, return negative points for the opponent (passive move)
        if passed:
            return -sum(card.get_score() for card in middle_cards)

        # If the opponent has no cards, the bot wins the current round and collects points
        if opponent_hand_size == 0 and is_initiative:
            return sum(card.get_score() for card in middle_cards)
        elif opponent_hand_size == 0 and not is_initiative:
            return -sum(card.get_score() for card in middle_cards)

        # Simulate bot's or opponent's move based on initiative (whose turn it is)
            # Try to simulate the bot playing a valid card
        valid_moves = [card for card in player_hand if self._is_playable(card, middle_cards, True)]
        if not valid_moves:
            return -sum(card.get_score() for card in middle_cards)
        played_card = random.choice(valid_moves)
        middle_cards += [played_card] 

        valid_moves_opp = [card for card in cards_in_the_deck if self._is_playable(card, middle_cards, True)]
        if not valid_moves_opp:
            return sum(card.get_score() for card in middle_cards)
        played_card_opp =  random.choice(valid_moves_opp)
        middle_cards += [played_card_opp] 

        return self._simulate_game(
            player_hand[:player_hand.index(played_card)] + player_hand[player_hand.index(played_card) + 1:],  # Remove played card
            middle_cards,  # Add played card to the middle
            cards_in_the_deck[cards_in_the_deck.index(played_card_opp)+1:] + cards_in_the_deck[:cards_in_the_deck.index(played_card_opp)],
            opponent_hand_size-1,            # Deck size decreases after playing a card
            is_initiative,                        # Change initiative to the opponent's turn
            passed                        # Bot didn't pass, so we don't penalize the score
        )
    