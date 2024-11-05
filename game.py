import random
import pygame
from tile import Tile
from dropping_tile import DroppingTile
from dropping_flag import DroppingFlag


class Game:
    def __init__(self, cols: int, rows: int, mine_count: int, tile_size: int=40) -> None:
        self.cols = cols
        self.rows = rows
        
        self.width = cols * tile_size
        self.height = rows * tile_size

        self.tile_size = tile_size
        self.mine_count = mine_count
        self.tiles = [[Tile(row, col, tile_size) for col in range(cols)] for row in range(rows)]
        

        self.dropping_tiles = []
        self.dropping_flags = []

        self.started = False
        self.lost = False

        pygame.font.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        self.digit_surfaces = get_digit_surfaces(tile_size)

    def draw_tiles(self, mouse_row, mouse_col):
        if pygame.mouse.get_focused():
            tile_hovered = self.tiles[mouse_row][mouse_col]
            tile_hovered.toggle_hover()

        for tile_row in self.tiles:
            for tile in tile_row:
                tile.draw(self.screen)

        if pygame.mouse.get_focused():
            tile_hovered.toggle_hover()
        

    def flip_tile(self, row: int, col: int):

        tile = self.tiles[row][col]

        if tile.is_flipped or tile.is_flagged:
            return

        self.dropping_tiles.append(DroppingTile(tile.x, tile.y, tile.size, tile.color))
        is_lost = tile.flip()
        if is_lost:
            self.lost = True


        if tile.mine_count == 0 and not self.lost:
            for neighbor in tile.neighbors:
                self.flip_tile(neighbor.row, neighbor.col)
    
    def start(self):
        pygame.init()
        pygame.display.set_caption("Minesweeper")

        while True:
            mouse = pygame.mouse.get_pos()
            col = mouse[0] // self.tile_size
            row = mouse[1] // self.tile_size

            self.handle_events(row, col)
            self.draw(row, col)
            self.clock.tick(60)

            if self.lost:
                self.lose()
                break

            if self.check_win():
                self.win()
                break

    def win(self):
        win_font = pygame.font.SysFont("Courrier", 100)
        win_surface = win_font.render("You Won!", True, "blue")
        win_rect = win_surface.get_rect(center=(self.width // 2, self.height // 2))

        while True:
            mouse = pygame.mouse.get_pos()
            col = mouse[0] // self.tile_size
            row = mouse[1] // self.tile_size
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                
                elif event.type == pygame.KEYDOWN and event.ket == pygame.K_q:
                    pygame.quit()

            self.screen.blit(win_surface, win_rect)
            pygame.display.update()
            self.clock.tick(60)


    def lose(self):
        count = 0
        col_auto = 0
        row_auto = 0

        self.remove_wrong_flags()

        while True:
            mouse = pygame.mouse.get_pos()
            col = mouse[0] // self.tile_size
            row = mouse[1] // self.tile_size

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                
                elif event.type == pygame.KEYDOWN and event.ket == pygame.K_q:
                    pygame.quit()

            self.draw(row, col)
            pygame.display.update()
            self.clock.tick(60)

            tile = self.tiles[row_auto][col_auto]

            if tile.has_mine and not tile.is_flipped:
                
                if tile.is_flagged:
                    tile.toggle_flag()
                    self.dropping_flags.append(DroppingFlag(tile.x, tile.y, tile.size))

                self.dropping_tiles.append(DroppingTile(tile.x, tile.y, tile.size, tile.color))
                tile.flip()

            count += 1

            col_auto = count % self.cols
            row_auto = count // self.rows

        
            if row_auto >= self.cols or col_auto >= self.rows:
                return

    def check_win(self):
        for tile_row in self.tiles:
            for tile in tile_row:
                if not (tile.is_flipped or tile.has_mine):
                    return False
        
        return True

    def draw(self, mouse_row, mouse_col):
        self.draw_tiles(mouse_row, mouse_col)
        self.draw_dropping_tiles()
        self.draw_falling_flags()
        pygame.display.update()

    def draw_dropping_tiles(self):
        for dropping_tile in self.dropping_tiles:
            dropping_tile.update()
            dropping_tile.draw(self.screen)

        for dropping_tile in self.dropping_tiles[::-1]:
            if dropping_tile.scale < 0.05:
                self.dropping_tiles.remove(dropping_tile)

        

    def draw_falling_flags(self):
        for dropping_flag in self.dropping_flags:
            dropping_flag.update()
            dropping_flag.draw(self.screen)

        for dropping_flag in self.dropping_flags[::-1]:
            if dropping_flag.scale < 0.05:
                self.dropping_flags.remove(dropping_flag)


    def handle_events(self, row, col):
        for event in pygame.event.get():
            self.handle_event(event, row, col)


    def handle_event(self, event, row, col):
        
        if event.type == pygame.QUIT:
            pygame.quit()
        
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            pygame.quit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.started:
            self.init_game(row, col)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            self.auto_flip_tile(row, col)
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            self.toggle_tile_flag(row, col)
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.flip_tile(row, col)


    def init_game(self, row, col):
        self.started = True
        self.generate_mines(row, col)
        self.set_tile_connections()
        self.set_tile_surfaces()


    def generate_mines(self, mouse_row, mouse_col, radius = 4):
        current_count = 0

        while current_count < self.mine_count:
            
            rand_row = random.randrange(0, self.rows)
            rand_col = random.randrange(0, self.cols)

            distance_x = abs(rand_row - mouse_row)
            distance_y = abs(rand_col - mouse_col)

            tile = self.tiles[rand_row][rand_col]

            if (distance_x < radius and distance_y < radius) or tile.has_mine:
                continue
            
            tile.has_mine = True
            current_count += 1

    def set_tile_connections(self):
        for tile_row in self.tiles:
            for tile in tile_row:
                tile.set_connections(self.tiles, self.cols, self.rows)


    def auto_flip_tile(self, row, col):
        tile = self.tiles[row][col]
        
        if not tile.is_flipped:
            return
    
        neighboring_flags_count = 0

        for neighbor in tile.neighbors:
            if neighbor.is_flagged:
                neighboring_flags_count += 1
        
        if neighboring_flags_count == tile.mine_count:
            for neighbor in tile.neighbors:
                self.flip_tile(neighbor.row, neighbor.col)

    def toggle_tile_flag(self, row, col):
        tile = self.tiles[row][col]
        if tile.is_flipped:
            return

        tile.toggle_flag()

        if tile.is_flagged == False:
            self.dropping_flags.append(DroppingFlag(tile.x, tile.y, tile.size))

    def set_tile_surfaces(self):
        for tile_row in self.tiles:
            for tile in tile_row:
                if tile.mine_count > 0 and not tile.has_mine:
                    tile.digit_surface = self.digit_surfaces[tile.mine_count]
    

    def remove_wrong_flags(self):
        for row in self.tiles:
            for tile in row:
                if tile.is_flagged and not tile.has_mine:
                    tile.toggle_flag()
                    self.dropping_flags.append(DroppingFlag(tile.x, tile.y, tile.size))

    
def get_digit_surfaces(size: int) -> None:

    pygame.font.init()

    font_size = int(size * 0.75)
    font = pygame.font.SysFont("Calibri", font_size, bold=True)

    digit_colors = ("blue", "forestgreen", "red", "purple", "orange", "black", "black", "black", "black")
 
    digit_surfaces = {}

    for digit, color in enumerate(digit_colors, 1):
        
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        digit_surface = font.render(str(digit), True, color)

        x = (size - digit_surface.get_width()) // 2
        y = (size - digit_surface.get_height()) // 2

        surface.blit(digit_surface, (x, y))

        digit_surfaces[digit] = surface
    
    return digit_surfaces
