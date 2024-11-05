import random
import pygame
from dropping_tile import DroppingTile


GREEN_LIGHT = pygame.Color(173, 232, 100)
GREEN_DARK = pygame.Color(153, 212, 80)
GREEN_HOVER = pygame.Color(213, 255, 122)
YELLOW_LIGHT = pygame.Color(247, 222, 176)
YELLOW_DARK = pygame.Color(237, 209, 159)
RED_FLAG = pygame.Color(255, 51, 51)

MINE_COLORS = (
    pygame.Color(252, 109, 0),
    pygame.Color(202, 252, 0),
    pygame.Color(0, 255, 140),
    pygame.Color(0, 247, 255),
    pygame.Color(132, 0, 255),
    pygame.Color(255, 0, 115)
)

class Tile:
    def __init__(self, row: int, col: int, size: int):
        self.row = row
        self.col = col
        self.size = size

        self.x = self.col * size
        self.y = self.row * size

        self.color = GREEN_DARK if (self.row + self.col) % 2 else GREEN_LIGHT

        self.has_mine = False
        self.is_flagged = False
        self.is_flipped = False
        self.is_hovered = False

        self.mine_count = 0
        self.digit_surface = None


    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

        if self.is_flagged:
            self.draw_flag(screen)
        
        elif self.is_flipped and self.digit_surface:
            screen.blit(self.digit_surface, (self.x, self.y))

    def draw_flag(self, screen):
        scaled_points = [(x + self.x + self.size // 2, y + self.y + self.size // 2) for x, y in DroppingFlag.points]
        
        pygame.draw.polygon(screen, RED_FLAG, scaled_points)


    def toggle_hover(self):
        self.is_hovered = not self.is_hovered

        if self.is_flipped:
            return
        
        if self.is_hovered:
            self.orig_color = self.color
            self.color = GREEN_HOVER
            return 
        
        self.color = self.orig_color
        

    def flip(self) -> bool:
        self.is_flipped = True
    
        if self.has_mine:
            self.color = random.choice(MINE_COLORS)
            return True
    
        self.color = YELLOW_DARK if (self.row + self.col) % 2 else YELLOW_LIGHT
        return False
        

    def toggle_flag(self):

        if self.is_flipped:
            return
        
        if self.is_flagged:
            self.is_flagged = False

        else:
            self.is_flagged = True

        

        
    def set_connections(self, tiles, cols: int, rows: int):
        self.neighbors = []
        mine_count = 0

        for row in range(max(0, self.row - 1),  min(self.row + 2, rows)):
            for col in range(max(0, self.col - 1),  min(self.col + 2, cols)):
                tile = tiles[row][col]
                self.neighbors.append(tile)

                if tile.has_mine:
                    mine_count += 1

        self.mine_count = mine_count



    def auto_flip(self):

        if not self.is_flipped:
            return

        marks_count = len([neighbor for neighbor in self.neighbors if neighbor.is_flagged])

        if marks_count == self.mine_count:
            for neighbor in self.neighbors:
                neighbor.flip_tile()

    


class DroppingFlag:
    points = (
        (-5, 15),
        (-5, 10),
        (-8, 10),
        (-8, 0),
        (15, -8),
        (-12, -18),
        (-12, 10),
        (-15, 10),
        (-15, 15),
        (-5, 15)
    )
