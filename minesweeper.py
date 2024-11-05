from game import Game

TILE_SIZE = 40

COLS = 20
ROWS = 20

MINE_COUNT = 50


if __name__ == "__main__":
    game = Game(COLS, ROWS, MINE_COUNT, TILE_SIZE)
    game.start()