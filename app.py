import pygame
import random
from enum import Enum

# Define Cards
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
        guess = random.choice(available_words) if available_words else None
        print(f"{self.name} of team {self.team} is guessing: {guess} based on clue: {clue}")
        return guess

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

    def reveal_card_by_word(self, word: str):
        for card in self.board.cards:
            if card.word == word and not card.revealed:
                card.reveal()
                return card
        return None

# ---------------------------
# Pygame GUI Integration
# ---------------------------

class GameGUI:
    def __init__(self, game: Game, screen_width=800, screen_height=800):
        self.game = game
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rows = 5
        self.cols = 5
        self.margin = 5
        # Calculate card dimensions for a grid layout
        self.card_width = (self.screen_width - (self.cols + 1) * self.margin) // self.cols
        self.card_height = (self.screen_height - (self.rows + 1) * self.margin) // self.rows

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("CodeNames GUI")
        self.font = pygame.font.SysFont("Arial", 18)
        self.running = True

    def draw_board(self):
        self.screen.fill((30, 30, 30))  # Background color

        for idx, card in enumerate(self.game.board.cards):
            row = idx // self.cols
            col = idx % self.cols
            x = self.margin + col * (self.card_width + self.margin)
            y = self.margin + row * (self.card_height + self.margin)
            rect = pygame.Rect(x, y, self.card_width, self.card_height)

            # Choose color based on whether the card has been revealed
            if card.revealed:
                if card.card_type == cardType.RED:
                    color = (255, 100, 100)
                elif card.card_type == cardType.BLUE:
                    color = (100, 100, 255)
                elif card.card_type == cardType.NEUTRAL:
                    color = (200, 200, 200)
                elif card.card_type == cardType.ASSASSIN:
                    color = (50, 50, 50)
                else:
                    color = (150, 150, 150)
            else:
                color = (70, 70, 70)  # Hidden card color

            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)

            # Render the card's word in the center
            text_surface = self.font.render(card.word, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)

    def get_card_at_position(self, pos):
        """Return the card at the given mouse position, or None if no card was clicked."""
        x, y = pos
        for idx, card in enumerate(self.game.board.cards):
            row = idx // self.cols
            col = idx % self.cols
            card_x = self.margin + col * (self.card_width + self.margin)
            card_y = self.margin + row * (self.card_height + self.margin)
            rect = pygame.Rect(card_x, card_y, self.card_width, self.card_height)
            if rect.collidepoint(x, y):
                return card
        return None

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    clicked_card = self.get_card_at_position(pos)
                    if clicked_card and not clicked_card.revealed:
                        clicked_card.reveal()
                        print(f"Revealed card: {clicked_card.word} ({clicked_card.card_type})")

            self.draw_board()
            pygame.display.flip()
            clock.tick(60) 

        pygame.quit()

# ---------------------------
# Main Entry Point
# ---------------------------
if __name__ == "__main__":
    # Sample list of 25+ words
    words = [
        "apple", "orange", "banana", "kiwi", "lemon", "grape", "peach", "berry", "melon", 
        "cherry", "plum", "pear", "mango", "papaya", "pineapple", "coconut", "lime", "apricot",
        "fig", "guava", "date", "nectarine", "passionfruit", "pomegranate", "dragonfruit"
    ]

    game = Game(words)
    gui = GameGUI(game)
    gui.run()
