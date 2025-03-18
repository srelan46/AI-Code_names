import pygame
from core.card import cardType
from config.constants import ROWS, COLS, MARGIN, SCREEN_HEIGHT, SCREEN_WIDTH

class EventHandler:
    def __init__(self, game_gui):
        self.gui = game_gui
        self.game = game_gui.game  # Store reference to game object
        self.running = True
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self._handle_resize(event)
            elif self.gui.mode == "clue" and event.type == pygame.KEYDOWN:
                self.process_clue_input(event)
            elif self.gui.mode == "guess" and event.type == pygame.MOUSEBUTTONDOWN:
                self.process_card(pos=pygame.mouse.get_pos())
            elif self.gui.mode == "guess" and event.type == pygame.KEYDOWN:
                self.process_card(key=event.unicode)
    
    def _handle_resize(self, event):
        self.gui.screen_width = event.w
        self.gui.screen_height = event.h
        self.gui.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        # Recalculate card dimensions
        self.gui.card_width = (event.w/1.5 - (COLS + 1) * MARGIN) // (COLS + 1)
        self.gui.card_height = (event.h/1.5 - (ROWS + 1) * MARGIN) // ROWS

    def process_clue_input(self, event):
        if event.key == pygame.K_RETURN:
            # When Enter is pressed, validate and set the clue.
            if self.game.validate_clue(self.gui.input_text):
                self.game.current_clue = self.gui.input_text .strip()
                try:
                    parts = self.gui.input_text .split(":", 1)
                    self.game.allowed_guesses = int(parts[1].strip())
                except Exception as e:
                    print("Error parsing allowed guesses:", e)
                    self.game.allowed_guesses = 0
                self.game.current_guess_count = 0
                print(f"Clue accepted: {self.game.current_clue}, allowed guesses: {self.game.allowed_guesses}")
                self.gui.mode = "guess"
                self.gui.input_text = ""
            else:
                print("Invalid clue. Please try again.")
                self.gui.input_text = ""  # Clear the input text to re-enter the clue
        elif event.key == pygame.K_BACKSPACE:
            self.gui.input_text  = self.gui.input_text [:-1]
        else:
            self.gui.input_text  += event.unicode
    
    def process_card(self, pos=None, key=None):
        if pos:
            clicked_card = self.get_card_at_position(pos)
        elif key and key.isalpha():
            idx = ord(key.lower()) - 97
            if 0 <= idx < len(self.game.board.cards):
                clicked_card = self.game.board.cards[idx]
            else:
                clicked_card = None
        else:
            clicked_card = None

        if clicked_card and not clicked_card.revealed:
            clicked_card.reveal()
            print(f"Revealed card: {clicked_card.word} ({clicked_card.card_type.value})")
            if clicked_card.card_type == cardType.ASSASSIN:
                print("Assassin card revealed! Game over!")
                self.gui.running = False
            elif clicked_card.card_type == cardType.NEUTRAL:
                print("Neutral card revealed. Switching turn.")
                self.gui.switch_turn_and_reset()
            elif clicked_card.card_type.value != self.game.current_team:
                print(f"{clicked_card.card_type.value.capitalize()} card revealed. Wrong guess!")
                if self.game.current_team == "red":
                    self.game.blue_score += 1
                else:
                    self.game.red_score += 1
                self.gui.switch_turn_and_reset()
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
                    self.gui.running = False
                elif self.game.blue_score >= 8:
                    print("Blue team wins!")
                    self.gui.running = False
                # If the allowed guesses have been reached, switch turn.
                elif self.game.current_guess_count >= self.game.allowed_guesses:
                    print("Allowed guesses reached. Switching turn.")
                    self.gui.switch_turn_and_reset()
    
    def get_card_at_position(self, pos):
        """Return the card at the given mouse position, or None if no card was clicked."""
        x, y = pos
        # Adjust for the top banner area (140 pixels)
        for idx, card in enumerate(self.game.board.cards):
            row = idx // COLS
            col = idx % COLS
            card_x = MARGIN + col * (self.gui.card_width + MARGIN)
            card_y = MARGIN + row * (self.gui.card_height + MARGIN) + 140
            rect = pygame.Rect(card_x, card_y, self.gui.card_width, self.gui.card_height)
            if rect.collidepoint(x, y):
                return card
        return None