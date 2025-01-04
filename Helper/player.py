class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.points = 0

    def draw(self, deck, num=1):
        """Draws a specified number of cards from the deck and adds them to the player's hand."""
        for _ in range(num):
            if len(deck) > 0:  # Check if the deck has cards
                self.hand.append(deck.draw_card())
            else:
                print("The deck is out of cards!")
                break

    def play_card(self, card_index):
        """Plays a card from the player's hand, given an index. Returns the played card."""
        if 0 <= card_index < len(self.hand):
            return self.hand.pop(card_index)
        else:
            print("Invalid card index. Please try again.")
            return None

    def show_hand(self):
        """Prints the player's current hand."""
        print(f"{self.name}'s hand:")
        for i, card in enumerate(self.hand):
            print(f"{i}: {card['rank']} of {card['suit']}")

    def has_cards(self):
        """Returns True if the player has cards in their hand, else False."""
        return len(self.hand) > 0
