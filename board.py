import pygame
from random import randint

TILE_EMPTY = 0
TILE_OBSTACLE = 1

TILE_COLOR = ["white", "gray"]


class GameBoard:
    def __init__(self, width, height, safe_zone_width):
        self.size = (width, height)
        self.safe_zone_width = safe_zone_width
        self.board = [[TILE_EMPTY for _ in range(height)] for _ in range(width)]

    def __random_danger__(self):
        x0 = self.safe_zone_width + 1
        x1 = self.size[0] - self.safe_zone_width - 1
        x, y = randint(x0, x1), randint(1, self.size[1] - 1)
        while self.board[x][y] != TILE_EMPTY:
            x, y = randint(x0, x1), randint(1, self.size[1] - 1)
        return x, y

    def add_obstacle(self, count=1):
        for _ in range(count):
            x, y = self.__random_danger__()
            self.board[x][y] = TILE_OBSTACLE

    def draw(self, window):
        surface = window.get_surface()
        window_width, window_height = window.get_size()
        width, height = self.size
        tile_width = window_width / width
        tile_height = window_height / height
        for x, column in enumerate(self.board):
            for y, tile in enumerate(column):
                color = TILE_COLOR[tile]
                if tile == TILE_EMPTY and (x < self.safe_zone_width or x > width - self.safe_zone_width):
                    color = "#efefef"

                rect = (x * tile_width, y * tile_height, tile_width, tile_height)
                pygame.draw.rect(surface, color, rect)
