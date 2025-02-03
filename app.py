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
        guess = random.choice(available_words) if available_words else ""
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

# ---------------------------
# Pygame GUI Integration
# ---------------------------
class GameGUI:
    def __init__(self, game: Game, screen_width=800, screen_height=900):
        self.game = game
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rows = 5
        self.cols = 5
        self.margin = 5
        # Calculate card dimensions for a grid layout
        self.card_width = (self.screen_width - (self.cols + 1) * self.margin) // self.cols
        self.card_height = (self.screen_width - (self.rows + 1) * self.margin) // self.rows

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("CodeNames GUI")
        self.font = pygame.font.SysFont("Arial", 18)
        self.running = True
        # Mode: "clue" for clue input, "guess" for operative guesses.
        self.mode = "clue"
        self.input_text = ""
    
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
        for card in self.game.board.cards:
            if not card.revealed and card.word.lower() == clue_word.lower():
                print(f"Clue word '{clue_word}' cannot be one of the unrevealed codenames.")
                return False

        # Validate the number is a digit
        if not clue_number.isdigit():
            print("The number part of the clue must be an integer.")
            return False

        return True

    def draw_board(self):
        # Fill background
        self.screen.fill((30, 30, 30))
        
        # Top banner area (allocated height 140 pixels)
        # Draw turn, mode, and score.
        turn_text = self.font.render(f"Turn: {self.game.current_team.capitalize()} Team", True, (255, 255, 0))
        self.screen.blit(turn_text, (10, 10))
        mode_text = self.font.render(f"Mode: {self.mode.capitalize()}", True, (255, 255, 0))
        self.screen.blit(mode_text, (10, 35))
        score_text = self.font.render(f"Score: Red {self.game.red_score} - Blue {self.game.blue_score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 60))
        
        if self.mode == "clue":
            # Draw the input text box for the spymaster's clue.
            input_box = pygame.Rect(10, 95, self.screen_width - 20, 30)
            pygame.draw.rect(self.screen, (50, 50, 50), input_box)
            pygame.draw.rect(self.screen, (255, 255, 255), input_box, 2)
            input_surface = self.font.render(self.input_text, True, (255, 255, 255))
            self.screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))
        elif self.mode == "guess" and self.game.current_clue:
            # Display the accepted clue and the allowed guess count.
            clue_display = self.font.render(f"Clue: {self.game.current_clue} (Allowed guesses: {self.game.allowed_guesses})", True, (255, 255, 255))
            self.screen.blit(clue_display, (10, 95))
        
        # Draw the grid of cards; offset y by 140 pixels to leave space for banner.
        for idx, card in enumerate(self.game.board.cards):
            row = idx // self.cols
            col = idx % self.cols
            x = self.margin + col * (self.card_width + self.margin)
            y = self.margin + row * (self.card_height + self.margin) + 140
            rect = pygame.Rect(x, y, self.card_width, self.card_height)

            # Choose color based on whether the card has been revealed.
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

            # Render the card's word in the center.
            text_surface = self.font.render(card.word, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)

    def get_card_at_position(self, pos):
        """Return the card at the given mouse position, or None if no card was clicked."""
        x, y = pos
        # Adjust for the top banner area (140 pixels)
        for idx, card in enumerate(self.game.board.cards):
            row = idx // self.cols
            col = idx % self.cols
            card_x = self.margin + col * (self.card_width + self.margin)
            card_y = self.margin + row * (self.card_height + self.margin) + 140
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

                # Clue mode: capture keyboard input for the spymaster's clue.
                elif self.mode == "clue" and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # When Enter is pressed, validate and set the clue.
                        if self.validate_clue(self.input_text):
                            self.game.current_clue = self.input_text.strip()
                            try:
                                parts = self.input_text.split(":", 1)
                                self.game.allowed_guesses = int(parts[1].strip())
                            except Exception as e:
                                print("Error parsing allowed guesses:", e)
                                self.game.allowed_guesses = 0
                            self.game.current_guess_count = 0
                            print(f"Clue accepted: {self.game.current_clue}, allowed guesses: {self.game.allowed_guesses}")
                            self.mode = "guess"
                            self.input_text = ""
                        else:
                            print("Invalid clue. Please try again.")
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        self.input_text += event.unicode

                # Guess mode: allow operative to click on cards.
                elif self.mode == "guess" and event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    clicked_card = self.get_card_at_position(pos)
                    if clicked_card and not clicked_card.revealed:
                        clicked_card.reveal()
                        print(f"Revealed card: {clicked_card.word} ({clicked_card.card_type.value})")
                        if clicked_card.card_type == cardType.ASSASSIN:
                            print("Assassin card revealed! Game over!")
                            self.running = False
                        elif clicked_card.card_type.value != self.game.current_team:
                            print(f"{clicked_card.card_type.value.capitalize()} card revealed. Wrong guess!")
                            self.game.switch_turn()
                            self.mode = "clue"
                            self.input_text = ""
                        else:
                            # Correct guess: increment the guess count and update score.
                            self.game.current_guess_count += 1
                            if self.game.current_team == "red":
                                self.game.red_score += 1
                            else:
                                self.game.blue_score += 1
                            print(f"Correct guess! {self.game.current_team.capitalize()} score updated.")
                            # Check win conditions.
                            if self.game.red_score >= 9:
                                print("Red team wins!")
                                self.running = False
                            elif self.game.blue_score >= 8:
                                print("Blue team wins!")
                                self.running = False
                            # If the allowed guesses have been reached, switch turn.
                            elif self.game.current_guess_count >= self.game.allowed_guesses:
                                print("Allowed guesses reached. Switching turn.")
                                self.game.switch_turn()
                                self.mode = "clue"
                                self.input_text = ""
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
    # Before the game starts, print the red and blue words (spymaster view)
    red_words = [card.word for card in game.board.cards if card.card_type == cardType.RED]
    blue_words = [card.word for card in game.board.cards if card.card_type == cardType.BLUE]
    print("Red team words:", red_words)
    print("Blue team words:", blue_words)

    gui = GameGUI(game)
    gui.run()
