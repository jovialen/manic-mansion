from window import Window, poll_events
from board import GameBoard
import pygame

TITLE = "Manic Mansion"
SIZE = (60, 40)
SAFE_ZONE_WIDTH = 10
RESOLUTION = (600, 400)


def main():
    pygame.init()
    window = Window("Manic Mansion", RESOLUTION)

    board = GameBoard(SIZE[0], SIZE[1], SAFE_ZONE_WIDTH)

    should_continue = True
    while poll_events() and should_continue:
        should_continue = board.update(window.get_delta_time())
        board.draw(window)
        window.update()

    pygame.quit()


if __name__ == "__main__":
    main()
