import random
import csv
from card import Card

class Deck:
    def __init__(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        self.cards = [Card(rank, suit) for suit in suits for rank in ranks]

    def __len__(self):
        return len(self.cards)
    
    def generate_deck(self):
        """Generates a deck of cards"""
        return [{'suit': suit, 'rank': rank} for suit in self.suits for rank in self.ranks]
        
    def shuffle_deck(self):
        """Shuffles the deck of cards"""
        random.shuffle(self.cards)
    
    def cut_deck(self, number):
        """Cuts the deck by moving the top 'number' of cards to the bottom of the deck."""
        self.cards = self.cards[number:] + self.cards[:number]
    
    def write_down_deck(self, filename='deck.csv'):
        self.deck = self.cards  # Store the current state of the deck
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Suit', 'Rank'])  # Write CSV headers
            for card in self.deck:
                writer.writerow([card.suit, card.rank])
        print("Deck written to", filename)
        
    def draw_card(self):
        return self.cards.pop() if self.cards else None
