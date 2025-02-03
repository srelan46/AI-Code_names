from Card import Card, cardType
import random
class Board:
    def __init__(self, words: list):
        self.cards: list[Card] = []
        self.setup_board(words)
    
    def setup_board(self, words: list):
        if len(words) < 25:
            raise ValueError("Not enough words to fill the board.")
        # Shuffle words
        selected_words = random.sample(words, 25)
        # Assign card types
        card_types = ([cardType.RED] * 9 + 
                      [cardType.BLUE] * 8 + 
                      [cardType.NEUTRAL] * 7 + 
                      [cardType.ASSASSIN] * 1)
        random.shuffle(card_types)
        
        # Create cards
        for word, card_type in zip(selected_words, card_types):
            self.cards.append(Card(word, card_type))