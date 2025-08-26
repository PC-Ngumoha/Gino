"""
main.py: Gino game.
"""
import pygame

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 720, 400
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Gino")


def main():
    """main code for the game.
    """
    game_running = True

    while game_running:
        # Poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

    pygame.quit()


if __name__ == '__main__':
    main()
