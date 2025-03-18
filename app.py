from gui.GameGUI import GameGUI
from core.game import Game
from core.card import cardType
from utils import read_words_from_file

if __name__ == "__main__":
    # Sample list of 25+ words
    words = read_words_from_file("words.txt")

    game = Game(words)
    # Before the game starts, print the red and blue words (spymaster view)
    red_words = [card.word for card in game.board.cards if card.card_type == cardType.RED]
    blue_words = [card.word for card in game.board.cards if card.card_type == cardType.BLUE]
    assassin_word = [card.word for card in game.board.cards if card.card_type == cardType.ASSASSIN]
    neutral_words = [card.word for card in game.board.cards if card.card_type == cardType.NEUTRAL]
    print("Red team words:", red_words)
    print("Blue team words:", blue_words)
    print("Assassin word:", assassin_word)
    print("Neutral words:", neutral_words)

    gui = GameGUI(game)
    gui.run()
