"""
main.py: Gino game.
"""
import pygame
import os

pygame.init()

# Constants


# Colors
WHITE = (255, 255, 255)

# Dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 720, 400

# Setup
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Gino")

# Images
HORIZON = pygame.image.load(os.path.join('Assets', 'sprites', 'Horizon.png'))


def draw_window():
    """Handles repainting of screen surface
    """
    WINDOW.fill(WHITE)
    WINDOW.blit(HORIZON, (0, SCREEN_HEIGHT//2))
    pygame.display.update()


def main():
    """main code for the game.
    """
    game_running = True

    while game_running:
        # Poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        draw_window()

    pygame.quit()


if __name__ == '__main__':
    main()
