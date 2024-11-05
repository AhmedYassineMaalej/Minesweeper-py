import pygame
import random
import numpy as np

RED_FLAG = pygame.Color(255, 51, 51)

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

    def __init__(self, x: int, y:int, size: int) -> None:

        self.pos = np.array([x + size // 2, y + size // 2], dtype=np.float64)
        self.velocity = np.array(
            [random.random() * 4 - 2, -3], dtype=np.float64
        )

        self.acceleration = np.array([0, 0.1 + 0.1 * random.random()])
        self.angle = 0
        self.speed_angle = random.random() * 0.02 + 0.02

        self.scale = 1
        self.speed_scale = 0.02

    
    def update(self):
        self.velocity += self.acceleration
        self.pos += self.velocity

        self.angle += self.speed_angle
        self.scale -= self.speed_scale
        
    
    def draw(self, screen):

        draw_points = []

        for x, y in DroppingFlag.points:

            draw_x = (x * np.cos(self.angle) - y * np.sin(self.angle)) * self.scale + self.pos[0]
            draw_y = (x * np.sin(self.angle) + y * np.cos(self.angle)) * self.scale + self.pos[1]
            draw_points.append((draw_x, draw_y))
        
        pygame.draw.polygon(screen, RED_FLAG, draw_points)