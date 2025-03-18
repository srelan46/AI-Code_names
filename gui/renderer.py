import pygame
from core.card import cardType
from config.colors import COLORS
from config.constants import ROWS, COLS, MARGIN

class Renderer:
    def __init__(self, game_gui):
        """Initialize renderer with reference to game GUI"""
        self.gui = game_gui
        self.screen = game_gui.screen
        self.fonts = {
            'title': game_gui.title_font,
            'card': game_gui.card_font,
            'info': game_gui.info_font
        }
        self.BANNER_HEIGHT = 140

    def draw_board(self):
        """Main drawing function that coordinates all rendering"""
        self._draw_background()
        self._draw_banner()
        self._draw_game_info()
        self._draw_input_area()
        self._draw_cards()
        pygame.display.flip()

    def _draw_background(self):
        """Draw the background color"""
        self.screen.fill(COLORS['background'])

    def _draw_banner(self):
        """Draw the top banner with gradient effect"""
        for i in range(self.BANNER_HEIGHT):
            alpha = 255 - int((i / self.BANNER_HEIGHT) * 155)
            color = (*COLORS['input_box'][:3], alpha)
            pygame.draw.line(self.screen, color, (0, i), (self.gui.screen_width, i))

    def _draw_game_info(self):
        """Draw game status information"""
        self._draw_turn_indicator()
        self._draw_mode_indicator()
        self._draw_score()

    def _draw_turn_indicator(self):
        """Draw the current team's turn indicator"""
        team_color = COLORS['red_team'] if self.gui.game.current_team == "red" else COLORS['blue_team']
        turn_text = self.fonts['title'].render(f"{self.gui.game.current_team.upper()} TEAM'S TURN", True, team_color)
        self.screen.blit(turn_text, (20, 15))

    def _draw_mode_indicator(self):
        """Draw the current game mode"""
        mode_text = self.fonts['info'].render(f"Mode: {self.gui.mode.capitalize()}", True, COLORS['text_light'])
        self.screen.blit(mode_text, (20, 55))

    def _draw_score(self):
        """Draw the score display"""
        score_text = self.fonts['info'].render("SCORE:", True, COLORS['text_light'])
        red_score = self.fonts['title'].render(str(self.gui.game.red_score), True, COLORS['red_team'])
        blue_score = self.fonts['title'].render(str(self.gui.game.blue_score), True, COLORS['blue_team'])
        
        score_x = self.gui.screen_width - 300
        self.screen.blit(score_text, (score_x, 20))
        self.screen.blit(red_score, (score_x + 100, 20))
        self.screen.blit(blue_score, (score_x + 200, 20))

    def _draw_input_area(self):
        """Draw the input box or clue display based on game mode"""
        if self.gui.mode == "clue":
            self._draw_clue_input()
        elif self.gui.mode == "guess" and self.gui.game.current_clue:
            self._draw_clue_display()

    def _draw_clue_input(self):
        """Draw the input box for entering clues"""
        input_box = pygame.Rect(20, 95, self.gui.screen_width - 40, 35)
        pygame.draw.rect(self.screen, COLORS['input_box'], input_box, border_radius=5)
        pygame.draw.rect(self.screen, COLORS['input_border'], input_box, 2, border_radius=5)
        
        placeholder = "Enter clue in format 'word:number'"
        text = self.gui.input_text if self.gui.input_text else placeholder
        text_color = COLORS['text_light'] if self.gui.input_text else COLORS['hidden']
        text_surface = self.fonts['info'].render(text, True, text_color)
        self.screen.blit(text_surface, (input_box.x + 10, input_box.y + 5))

    def _draw_clue_display(self):
        """Draw the current clue and remaining guesses"""
        clue_text = self.fonts['info'].render(
            f"CLUE: {self.gui.game.current_clue.upper()} ({self.gui.game.allowed_guesses - self.gui.game.current_guess_count} guesses remaining)", 
            True, 
            COLORS['text_light']
        )
        self.screen.blit(clue_text, (20, 95))

    def _draw_cards(self):
        """Draw all cards on the board"""
        for idx, card in enumerate(self.gui.game.board.cards):
            self._draw_single_card(idx, card)

    def _draw_single_card(self, idx, card):
        """Draw a single card with all its visual elements"""
        row = idx // ROWS
        col = idx % COLS
        x = MARGIN + col * (self.gui.card_width + MARGIN)
        y = MARGIN + row * (self.gui.card_height + MARGIN) + self.BANNER_HEIGHT
        
        rect = pygame.Rect(x, y, self.gui.card_width, self.gui.card_height)
        color = self._get_card_color(card)
        
        self._draw_card_shadow(rect)
        self._draw_card_base(rect, color)
        self._draw_card_gradient(rect, color)
        self._draw_card_content(card, rect, idx)

    def _get_card_color(self, card):
        """Get the color for a card based on its type and revealed state"""
        if not card.revealed:
            return COLORS['hidden']
        
        color_map = {
            cardType.RED: COLORS['red_team'],
            cardType.BLUE: COLORS['blue_team'],
            cardType.NEUTRAL: COLORS['neutral'],
            cardType.ASSASSIN: COLORS['assassin']
        }
        return color_map[card.card_type]

    def _draw_card_shadow(self, rect, offset=3):
        """Draw shadow effect for a card"""
        shadow_rect = rect.copy()
        shadow_rect.x += offset
        shadow_rect.y += offset
        pygame.draw.rect(self.screen, (0, 0, 0, 64), shadow_rect, border_radius=10)

    def _draw_card_base(self, rect, color):
        """Draw the main background of a card"""
        pygame.draw.rect(self.screen, color, rect, border_radius=10)

    def _draw_card_gradient(self, rect, color):
        """Draw gradient effect on a card"""
        gradient_rect = rect.copy()
        gradient_rect.height = rect.height // 2
        pygame.draw.rect(self.screen, (*color, 128), gradient_rect, border_radius=10)

    def _draw_card_content(self, card, rect, idx):
        """Draw the word and number on a card"""
        text_color = (COLORS['text_dark'] 
                     if card.revealed and card.card_type == cardType.NEUTRAL 
                     else COLORS['text_light'])
        
        # Draw word
        text_surface = self.fonts['card'].render(card.word.upper(), True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
        
        # Draw card number
        number_surface = self.fonts['info'].render(chr(idx + 97), True, text_color)
        number_rect = number_surface.get_rect(topright=(rect.right - 8, rect.top + 8))
        self.screen.blit(number_surface, number_rect)