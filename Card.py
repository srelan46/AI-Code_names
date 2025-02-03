from enum import Enum
class cardType(Enum):
    RED = 'red'
    BLUE = 'blue'
    NEUTRAL = 'neutral'
    ASSASSIN = 'assassin'

class Card:
    def __init__(self, word: str, card_type: cardType):
        self.word = word
        self.card_type = card_type
        self.revealed = False

    def reveal(self):
        self.revealed = True    
    
    def __repr__(self):
        status = "revealed" if self.revealed else "hidden"
        return f"Card({self.word}, {self.card_type.value}, {status})"