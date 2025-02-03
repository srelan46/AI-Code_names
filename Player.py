from Board import Board
import random

class Player:
    def __init__(self, name: str, role: str, team: str):
        self.name = name
        self.role = role
        self.team = team
    
    def give_hint(self, board: Board) -> str:
        clue = f"Clue from {self.name}"
        print(f"{self.name} is generating a clue: {clue} for {self.team} team")
        return clue

    def guess_word(self, board: Board, clue: str) -> str:
        available_words = [card.word for card in board.cards if not card.revealed]
        guess = random.choice(available_words) if available_words else ""
        print(f"{self.name} of team {self.team} is guessing: {guess} based on clue: {clue}")
        return guess