from Board import Board
from Player import Player

class Game:
    def __init__(self, words: list):
        self.board = Board(words)
        # Initialize four players (red and blue teams, each with spymaster and operative)
        self.players = [
            Player("Player_Red_Spymaster", "spymaster", "red"),
            Player("Player_Red_Operative", "operative", "red"),
            Player("Player_Blue_Spymaster", "spymaster", "blue"),
            Player("Player_Blue_Operative", "operative", "blue")
        ]
        # Assume red starts (for example)
        self.current_team = "red"
        self.current_clue = None
        # New attributes for guess management and scoring:
        self.allowed_guesses = 0
        self.current_guess_count = 0
        self.red_score = 0
        self.blue_score = 0

    def switch_turn(self):
        self.current_team = "blue" if self.current_team == "red" else "red"
        self.current_clue = None
        self.allowed_guesses = 0
        self.current_guess_count = 0
        print(f"Switching turn. It's now {self.current_team} team's turn.")

    def reveal_card_by_word(self, word: str):
        for card in self.board.cards:
            if card.word == word and not card.revealed:
                card.reveal()
                return card
        return None