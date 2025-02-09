from GameGUI import GameGUI
from Game import Game
from Card import cardType
from utils import read_words_from_file

if __name__ == "__main__":
    # Sample list of 25+ words
    words = read_words_from_file("words.txt")

    game = Game(words)
    # Before the game starts, print the red and blue words (spymaster view)
    red_words = [card.word for card in game.board.cards if card.card_type == cardType.RED]
    blue_words = [card.word for card in game.board.cards if card.card_type == cardType.BLUE]
    print("Red team words:", red_words)
    print("Blue team words:", blue_words)

    gui = GameGUI(game)
    gui.run()
