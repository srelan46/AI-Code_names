from core.board import Board
import random
from LLM import generate_clue_with_llm
class Player:
    def __init__(self, name: str, role: str, team: str, llm_type: str = "gpt-4o"):
        self.name = name
        self.role = role
        self.team = team
        self.llm_type = llm_type
    
    def give_hint(self, board: Board) -> str:
        unrevealed_cards = [card for card in board.cards if not card.revealed]
        if self.llm_type:
            clue = generate_clue_with_llm(unrevealed_cards,self.team,self.llm_type)
        else:
            clue = f"Clue from {self.name}"
        print(f"{self.name} is generating a clue: {clue} for {self.team} team")
        return clue

    def guess_word(self, board: Board, clue: str) -> str:
        available_words = [card.word for card in board.cards if not card.revealed]
        guess = random.choice(available_words) if available_words else ""
        print(f"{self.name} of team {self.team} is guessing: {guess} based on clue: {clue}")
        return guess