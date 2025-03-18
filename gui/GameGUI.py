from pathlib import Path
import pygame
import os
from core.card import cardType
from core.game import Game
from gui.event_handler import EventHandler
from gui.renderer import Renderer
from config import colors
from config.constants import ROWS,COLS,MARGIN,SCREEN_HEIGHT,SCREEN_WIDTH

class GameGUI:
    def __init__(self, game: Game, screen_width=1920, screen_height=1080):
        self.game = game
        
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

        # Calculate card dimensions for a grid layout
        self.card_width = (self.screen_width/1.5 - (COLS + 1) * MARGIN) // (COLS +1)
        self.card_height = (self.screen_height/1.5 - (ROWS + 1) * MARGIN) // ROWS

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption("CodeNames GUI")
        self.font = pygame.font.SysFont("Arial", 18)
        self.running = True
        # Mode: "clue" for clue input, "guess" for operative guesses.
        self.mode = "clue"
        self.input_text = ""
        self.colors = colors
        self._load_fonts()

        self.renderer = Renderer(self)
        self.event_handler = EventHandler(self)

    def _load_fonts(self):
        # Load fonts
        try:
            font_path = os.path.join(Path(__file__).parent, "assets", "fonts")
            self.title_font = pygame.font.Font(os.path.join(font_path, "Roboto-Bold.ttf"), 32)
            self.card_font = pygame.font.Font(os.path.join(font_path, "Roboto-Medium.ttf"), 20)
            self.info_font = pygame.font.Font(os.path.join(font_path, "Roboto-Regular.ttf"), 24)
        except:
            print("Using system fonts as fallback")
            self.title_font = pygame.font.SysFont("Arial", 32)
            self.card_font = pygame.font.SysFont("Arial", 20)
            self.info_font = pygame.font.SysFont("Arial", 24)
    
    def switch_turn_and_reset(self):
        self.game.switch_turn()
        self.mode = "clue"
        self.input_text = ""

    def draw_board(self):
        """Delegate board drawing to renderer"""
        self.renderer.draw_board()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.event_handler.handle_events()
            self.draw_board()
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()