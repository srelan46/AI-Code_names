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

    def validate_clue(self, clue_str: str) -> bool:
        """
        Validates that the clue is in the format "word:number", that the word has no spaces,
        and that the clue word is not one of the unrevealed codenames on the board.
        """
        if ":" not in clue_str:
            print("Clue must contain a colon separating the word and the number (e.g., tree:2).")
            return False
        parts = clue_str.split(":", 1)
        clue_word = parts[0].strip()
        clue_number = parts[1].strip()

        # Check that the clue word is a single word (no spaces)
        if " " in clue_word or not clue_word:
            print("Clue must be a single word with no spaces.")
            return False

        # Ensure the clue word is not among the unrevealed card words (case-insensitive)
        for card in self.board.cards:
            if not card.revealed and card.word.lower() == clue_word.lower():
                print(f"Clue word '{clue_word}' cannot be one of the unrevealed codenames.")
                return False

        # Validate the number is a digit
        if not clue_number.isdigit():
            print("The number part of the clue must be an integer.")
            return False

        # Check if allowed guesses are less than or equal to the winning condition
        allowed_guesses = int(clue_number)
        if self.current_team == "red" and allowed_guesses > (9 - self.red_score):
            print("Allowed guesses exceed the winning condition for the Red team.")
            return False
        elif self.current_team == "blue" and allowed_guesses > (8 - self.blue_score):
            print("Allowed guesses exceed the winning condition for the Blue team.")
            return False

        return True