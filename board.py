import pygame

TILE_EMPTY = 0

TILE_COLOR = ["white", "gray"]


class GameBoard:
    def __init__(self, width, height, safe_zone_width):
        self.size = (width, height)
        self.safe_zone_width = safe_zone_width
        self.board = [[0] * height] * width

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
