import pygame
import random
from enum import Enum
from Card import Card, cardType
from Game import Game

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