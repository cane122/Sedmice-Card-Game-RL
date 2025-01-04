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
            cards_in_the_deck: List of remaining cards in deck
            opponent_hand_size: Number of cards in opponent's hand
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
            # Create deep copies for simulation
            deck_copy = deepcopy(cards_in_the_deck)
            
            # Try each possible move
            for i, card in enumerate(player_hand):
                if self._is_playable(card, card_in_middle, is_initiative):
                    # Simulate game after playing this card
                    strategic_penalty = self._calculate_penalty(card)
                    
                    # Create new simulation state
                    new_player_hand = player_hand[:i] + player_hand[i+1:]
                    new_middle = [card] if not card_in_middle else card_in_middle + [card]
                    
                    score = self._simulate_game(
                        deepcopy(new_player_hand),
                        new_middle,
                        deepcopy(deck_copy),
                        opponent_hand_size,
                        is_initiative
                    )
                    move_scores[i] += (score - strategic_penalty)

            # Simulate passing if we have initiative and there's a card in middle
            if is_initiative and card_in_middle:
                pass_score += -sum(card.get_score() for card in card_in_middle)

        # Average the scores
        for move in move_scores:
            move_scores[move] /= self.num_simulations
        if is_initiative and card_in_middle:
            pass_score /= self.num_simulations

        # Find best move
        best_move_score = max(move_scores.values(), default=-float('inf'))
        
        # If passing is better than playing any card
        if pass_score > best_move_score and is_initiative and card_in_middle:
            return None, True

        # Find the best card to play
        best_moves = [i for i, score in move_scores.items() 
                     if score == best_move_score and 
                     self._is_playable(player_hand[i], card_in_middle, is_initiative)]

        if best_moves:
            return random.choice(best_moves), False
        return None, True
    
    def _calculate_penalty(self, card):
        """Calculate strategic penalty for playing certain cards."""
        return 10 if card.rank == "7" else 0
    
    def _is_playable(self, card, card_in_middle, is_initiative):
        """Check if a card is playable in the current state."""
        if not card_in_middle:
            return True
        if not is_initiative:
            return True
        if card.rank == "7":
            return True
        return card.rank == card_in_middle[-1].rank if card_in_middle else True

    def _simulate_game(self, player_hand, middle_cards, deck, opponent_hand_size, is_initiative):
        """Simulate a game from the current state."""
        score = 0
        # Create opponent's initial hand
        opp_hand = []
        while len(opp_hand) < opponent_hand_size and deck:
            opp_hand.append(deck.pop(random.randrange(len(deck))))

        while deck or player_hand or opp_hand:
            # Draw cards if needed
            while len(player_hand) < 4 and deck:
                player_hand.append(deck.pop(random.randrange(len(deck))))
                opp_hand.append(deck.pop(random.randrange(len(deck))))
            
            # Play the hand
            hand_score, player_hand, opp_hand = self._play_hand(
                player_hand, opp_hand, middle_cards.copy(), is_initiative,is_initiative
            )
            middle_cards = []
            score += hand_score
            
            if not player_hand and not deck:
                break
                
        return score
    
    def _play_hand(self, player_hand, opp_hand, middle_cards, is_initiative, turn):
        """Simulate playing a single hand."""
        if not player_hand and not opp_hand:
            return (sum(card.get_score() for card in middle_cards) if is_initiative 
                   else -sum(card.get_score() for card in middle_cards)), player_hand, opp_hand
        print( player_hand)
        print(opp_hand)
        print(middle_cards)
        print(is_initiative)
        print(turn)
        if turn:
            # Bot's turn
            valid_moves = [card for card in player_hand if self._is_playable(card, middle_cards, is_initiative)]
            if not valid_moves and is_initiative:
                return -sum(card.get_score() for card in middle_cards), player_hand, opp_hand
            if not valid_moves:
                played_card = random.choice(valid_moves)
                new_player_hand = [c for c in player_hand if c != played_card]
                middle_cards.append(played_card)
            if valid_moves:
                played_card = random.choice(player_hand)
                new_player_hand = [c for c in player_hand if c != played_card]
                middle_cards.append(played_card)
            return self._play_hand(new_player_hand, opp_hand, middle_cards,is_initiative, False)
        else:
            # Opponent's turn
            valid_moves = [card for card in opp_hand if self._is_playable(card, middle_cards, not is_initiative)]
            if not valid_moves and not is_initiative:
                return sum(card.get_score() for card in middle_cards), player_hand, opp_hand
            if not valid_moves:
                played_card = random.choice(valid_moves)
                new_opp_hand = [c for c in opp_hand if c != played_card]
                middle_cards.append(played_card)
            else:
                played_card = random.choice(opp_hand)
                new_opp_hand = [c for c in opp_hand if c != played_card]
                middle_cards.append(played_card)
            
            return self._play_hand(player_hand, new_opp_hand, middle_cards,is_initiative, True)