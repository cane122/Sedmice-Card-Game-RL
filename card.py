class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank} of {self.suit}"
    
    def get_score(self):
        if self.rank in ["Ace",'10']:
            return 10
        return 0