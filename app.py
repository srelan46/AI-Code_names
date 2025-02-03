from GameGUI import GameGUI
from Game import Game
from Card import cardType

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
