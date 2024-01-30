from window import Window, poll_events
import pygame

TITLE = "Manic Mansion"
SIZE = (600, 400)


def main():
    pygame.init()
    window = Window("Manic Mansion", SIZE)
    while poll_events():
        window.update()
    pygame.quit()


if __name__ == "__main__":
    main()