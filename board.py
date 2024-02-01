import pygame
from random import randint, choice

TILE_EMPTY = 0
TILE_OBSTACLE = 1
TILE_GHOST = 2
TILE_SHEEP = 3
TILE_PLAYER = 4

TILE_COLOR = ["white", "gray", "red", "blue", "green"]


class GameBoard:
    def __init__(self, width, height, safe_zone_width):
        self.size = (width, height)
        self.safe_zone_width = safe_zone_width
        self.board = [[TILE_EMPTY for _ in range(height)] for _ in range(width)]
        self.ghosts = []
        self.has_sheep = False

        self.add_obstacle(3)
        self.add_ghost(1)
        self.add_sheep(3)

        self.player = self.__random_safe__(False)
        self.move_timer = 0
        self.is_player_move = True
        self.board[self.player[0]][self.player[1]] = TILE_PLAYER

    def __random_danger__(self):
        x0 = self.safe_zone_width + 1
        x1 = self.size[0] - self.safe_zone_width - 1
        x, y = randint(x0, x1), randint(0, self.size[1] - 1)
        while self.board[x][y] != TILE_EMPTY:
            x, y = randint(x0, x1), randint(0, self.size[1] - 1)
        return x, y

    def __random_safe__(self, right_side):
        x0 = 0
        x1 = self.safe_zone_width
        x, y = randint(x0, x1), randint(0, self.size[1] - 1)
        while self.board[x][y] != TILE_EMPTY:
            x, y = randint(x0, x1), randint(0, self.size[1] - 1)
        if right_side:
            x = self.size[0] - x - 1
        return x, y

    def add_obstacle(self, count=1):
        for _ in range(count):
            x, y = self.__random_danger__()
            self.board[x][y] = TILE_OBSTACLE

    def add_ghost(self, count=1):
        for _ in range(count):
            x, y = self.__random_danger__()
            y = max(min(y, self.size[1] - 2), 1)  # Don't allow spawning on edges
            self.board[x][y] = TILE_GHOST
            self.ghosts.append((x, y, choice([-1, 1]), choice([-1, 1])))

    def add_sheep(self, count=1):
        for _ in range(count):
            x, y = self.__random_safe__(True)
            self.board[x][y] = TILE_SHEEP

    def __level_up__(self):
        self.add_sheep()
        self.add_ghost()
        self.add_obstacle()

    def move_player(self, mx, my):
        x, y = self.player
        nx, ny = x + mx, y + my
        if nx < 0 or nx >= self.size[0] or ny < 0 or ny >= self.size[1]:
            return False
        elif self.board[nx][ny] == TILE_OBSTACLE:
            return False
        elif self.board[nx][ny] == TILE_SHEEP:
            if self.has_sheep:
                return False
            self.has_sheep = True
        elif nx <= self.safe_zone_width and self.has_sheep:
            self.has_sheep = False
            self.__level_up__()
        self.board[x][y] = TILE_EMPTY
        self.board[nx][ny] = TILE_PLAYER
        self.player = (nx, ny)
        return any(map(lambda ghost: ghost[0] == nx and ghost[1] == ny, self.ghosts))

    def __update_ghosts__(self):
        for i in range(len(self.ghosts)):
            x, y, mx, my = self.ghosts[i]
            if self.board[x][y] != TILE_OBSTACLE:
                self.board[x][y] = TILE_EMPTY
            nx, ny = x + mx, y + my
            if ny == 0 or ny == self.size[1] - 1:
                my *= -1
            if nx <= self.safe_zone_width + 1 or nx >= self.size[0] - self.safe_zone_width - 1:
                mx *= -1
            self.ghosts[i] = (nx, ny, mx, my)
            self.board[nx][ny] = self.board[nx][ny] or TILE_GHOST

    def __update_player__(self):
        keys = pygame.key.get_pressed()
        mx, my = 0, 0
        if keys[pygame.K_w]:
            my = -1
        elif keys[pygame.K_s]:
            my = 1
        if keys[pygame.K_d]:
            mx = 1
        elif keys[pygame.K_a]:
            mx = -1
        died = self.move_player(mx, my)
        return not died

    def update(self, dt):
        self.move_timer += dt
        if self.move_timer < 0.1:
            return True
        self.move_timer = 0

        self.__update_ghosts__()

        self.is_player_move = not self.is_player_move
        self.is_player_move |= not self.has_sheep
        if self.is_player_move:
            return self.__update_player__()
        else:
            return True

    def draw(self, window):
        surface = window.get_surface()
        window_width, window_height = window.get_size()
        width, height = self.size
        tile_width = window_width / width
        tile_height = window_height / height
        for x, column in enumerate(self.board):
            for y, tile in enumerate(column):
                color = TILE_COLOR[tile]
                if tile == TILE_EMPTY and (x <= self.safe_zone_width or x >= width - self.safe_zone_width):
                    color = "#efefef"

                rect = (x * tile_width, y * tile_height, tile_width, tile_height)
                pygame.draw.rect(surface, color, rect)
