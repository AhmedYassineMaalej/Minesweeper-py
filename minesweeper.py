import pygame
import random

TILE_DIMENSION = 40

WIDTH_TILES = 20
HEIGHT_TILES = 20
NUM_MINES = 40

WIDTH_SCREEN = WIDTH_TILES * TILE_DIMENSION
HEIGHT_SCREEN = HEIGHT_TILES * TILE_DIMENSION

GREEN_LIGHT = pygame.Color(173, 232, 100)
GREEN_DARK = pygame.Color(153, 212, 80)
GREEN_HOVER = pygame.Color(213, 255, 122)
YELLOW_LIGHT = pygame.Color(247, 222, 176)
YELLOW_DARK = pygame.Color(237, 209, 159)

pygame.font.init()
font = pygame.font.SysFont("calibri", 30, bold=True)

ONE = font.render("1", True, "blue")
TWO = font.render("2", True, "green3")
THREE = font.render("3", True, "red")
FOUR = font.render("4", True, "purple")
FIVE = font.render("5", True, "orange")
SIX = font.render("6", True, "black")

NUMBER_SURFACES = {
    1: ONE,
    2: TWO,
    3: THREE,
    4: FOUR,
    5: FIVE,
    6: SIX
}

ARROW_POINTS = [
    (10, 10),
    (10, 5),
    (2, 5),
    (2, -10),
    (15, -15),
    (-2, -25),
    (-2, 5),
    (-10, 5),
    (-10, 10), 
    (10, 10)
]


class Tile:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

        self.x = self.col * TILE_DIMENSION
        self.y = self.row * TILE_DIMENSION

        self.has_mine = False
        self.is_flipped = False
        self.is_flagged = False
        
        self.set_color()

        self.neighbors = []
        

    def set_color(self):
        parity = (self.row + self.col) % 2

        if parity == 0:
            self.color = GREEN_LIGHT
            self.flip_color = YELLOW_LIGHT
        
        else:
            self.color = GREEN_DARK
            self.flip_color = YELLOW_DARK
         

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, TILE_DIMENSION, TILE_DIMENSION))

        if self.is_flipped and self.number != 0:
            text = NUMBER_SURFACES[self.number]
            screen.blit(text, (self.x + 10, self.y + 7))
        
        if self.is_flagged and not self.is_flipped:
            draw_arrow(self.x + TILE_DIMENSION / 2, self.y + TILE_DIMENSION // 2)


    def draw_hovered(self):
        if self.is_flipped:
            return
        
        pygame.draw.rect(screen, GREEN_HOVER, (self.x, self.y, TILE_DIMENSION, TILE_DIMENSION))


    def flip(self):
        if self.is_flipped or self.is_flagged:
            return
        
        self.is_flipped = True
        self.color = self.flip_color

        if self.has_mine:
            self.color = "red"

        if self.number != 0:
            return

        for tile in self.neighbors:
            tile.flip()


    def set_connections(self):

        min_row = max(0, self.row-1)
        max_row = min(HEIGHT_TILES, self.row+2)
        min_col = max(0, self.col-1)
        max_col = min(HEIGHT_TILES, self.col+2)

        for r in range(min_row, max_row):
            for c in range(min_col, max_col):
                self.neighbors.append(tiles[r][c])    
            
        self.neighbors.remove(self)
        self.set_number()


    def set_number(self):
        count = 0

        for tile in self.neighbors:
            if tile.mine:
                count += 1
        
        self.number = count


    def toggle_mark(self):
        self.is_flagged = not self.is_flagged

    def __repr__(self) -> str:
        return f"<Tile Object: row: {self.row}, col: {self.col}, mine: {self.has_mine}>"


pygame.init()
pygame.display.set_caption("Minesweeper")
clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))

GAME = False
tiles:list[list[Tile]] = []

# Populating list
for row in range(HEIGHT_TILES):
    row_list = []

    for col in range(WIDTH_TILES):
        row_list.append(Tile(row, col))
    
    tiles.append(row_list)


def draw_arrow(draw_x, draw_y):
    points = [(x + draw_x, y + draw_y) for x,y in ARROW_POINTS]

    pygame.draw.polygon(screen, "red", points)


def draw_tiles():

    screen.fill("black")

    for row in range(HEIGHT_TILES):
        for col in range(WIDTH_TILES):

            tile = tiles[row][col]
            tile.draw()


    # check in mouse in game screen:
    if pygame.mouse.get_focused():
        
        mouse = pygame.mouse.get_pos()
        draw_hover(mouse)


    pygame.display.update()


def draw_hover(mouse: tuple[int, int]) -> None:
    
    col = mouse[0] // TILE_DIMENSION
    row = mouse[1] // TILE_DIMENSION

    hovered_tile:Tile = tiles[row][col]
    if hovered_tile.is_flipped:
        return

    og_color = hovered_tile.color
    hovered_tile.color = GREEN_HOVER
    hovered_tile.draw()
    hovered_tile.color = og_color


def add_mine(mouse_row, mouse_col):

    row = random.randrange(0, HEIGHT_TILES)
    col = random.randrange(0, WIDTH_TILES)

    tile = tiles[row][col]

    if tile.has_mine or (row == mouse_row and col == mouse_col):
        return add_mine(mouse_row, mouse_col)


    tile.has_mine = True


def generate_minefield():

    mouse = pygame.mouse.get_pos()

    col = mouse[0] // TILE_DIMENSION
    row = mouse[1] // TILE_DIMENSION

    for _ in range(NUM_MINES):
        add_mine(row, col)


def click_tile():
    
    mouse = pygame.mouse.get_pos()

    col = mouse[0] // TILE_DIMENSION
    row = mouse[1] // TILE_DIMENSION

    tile = tiles[row][col]
    tile.flip()


def start_game():
    global GAME

    GAME = True
    
    generate_minefield()
    connect_tiles()


def mark_tile():
    mouse = pygame.mouse.get_pos()

    col = mouse[0] // TILE_DIMENSION
    row = mouse[1] // TILE_DIMENSION

    tile = tiles[row][col]
    tile.toggle_mark()

def handle_events():

    for ev in pygame.event.get():

        if ev.type == pygame.QUIT:
            pygame.quit()

        elif ev.type == pygame.MOUSEBUTTONDOWN:
            
            # LEFT CLICK
            if ev.button == 1:

                if GAME == False:
                    start_game()
                    

                click_tile()
            
            elif ev.button == 3:
                mark_tile()


        elif ev.type == pygame.KEYDOWN:

            if ev.key == pygame.K_q:
                pygame.quit()


def connect_tiles():
    for row in range(HEIGHT_TILES):
        for col in range(WIDTH_TILES):

            tiles[row][col].set_connections()


     
def main():
    global GAME

    while True:

        handle_events()

        draw_tiles()

        clock.tick()

main()

