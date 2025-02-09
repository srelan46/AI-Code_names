import pygame
from Card import cardType
from Game import Game

class GameGUI:
    def __init__(self, game: Game, screen_width=1920, screen_height=1080):
        self.game = game
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rows = 5
        self.cols = 5
        self.margin = 5
        # Calculate card dimensions for a grid layout
        self.card_width = (self.screen_width/1.5 - (self.cols + 1) * self.margin) // (self.cols +1)
        self.card_height = (self.screen_height/1.5 - (self.rows + 1) * self.margin) // self.rows

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("CodeNames GUI")
        self.font = pygame.font.SysFont("Arial", 18)
        self.running = True
        # Mode: "clue" for clue input, "guess" for operative guesses.
        self.mode = "clue"
        self.input_text = ""
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.screen_width, self.screen_height = event.w, event.h
                self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
                # Recalculate card dimensions
                self.card_width = (self.screen_width/1.5 - (self.cols + 1) * self.margin) // (self.cols + 1)
                self.card_height = (self.screen_height/1.5 - (self.rows + 1) * self.margin) // self.rows
            elif self.mode == "clue" and event.type == pygame.KEYDOWN:
                self.process_clue_input(event)
            elif self.mode == "guess" and event.type == pygame.MOUSEBUTTONDOWN:
                self.process_card_click()

    def switch_turn_and_reset(self):
        self.game.switch_turn()
        self.mode = "clue"
        self.input_text = ""

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

    def process_clue_input(self, event):
        if event.key == pygame.K_RETURN:
            # When Enter is pressed, validate and set the clue.
            if self.game.validate_clue(self.input_text):
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
                self.input_text = ""  # Clear the input text to re-enter the clue
        elif event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        else:
            self.input_text += event.unicode
        
    def process_card_click(self):
        pos = pygame.mouse.get_pos()
        clicked_card = self.get_card_at_position(pos)
        if clicked_card and not clicked_card.revealed:
            clicked_card.reveal()
            print(f"Revealed card: {clicked_card.word} ({clicked_card.card_type.value})")
            if clicked_card.card_type == cardType.ASSASSIN:
                print("Assassin card revealed! Game over!")
                self.running = False
            elif clicked_card.card_type == cardType.NEUTRAL:
                print("Neutral card revealed. Switching turn.")
                self.switch_turn_and_reset()
            elif clicked_card.card_type.value != self.game.current_team:
                print(f"{clicked_card.card_type.value.capitalize()} card revealed. Wrong guess!")
                if self.game.current_team == "red":
                    self.game.blue_score += 1
                else:
                    self.game.red_score += 1
                self.switch_turn_and_reset()
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
                    self.switch_turn_and_reset()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.draw_board()
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()