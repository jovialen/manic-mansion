import pygame


def poll_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


class Window:
    def __init__(self, title, size, fps=60.0, clear_color="white"):
        pygame.display.set_caption(title)
        self.size = size
        self.window = pygame.display.set_mode(size)
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.clear_color = clear_color

    def update(self):
        pygame.display.flip()
        self.window.fill(self.clear_color)
        self.dt = self.clock.tick(self.fps) / 1000

    def get_size(self):
        return self.size

    def get_delta_time(self):
        return self.dt

    def get_surface(self):
        return self.window
