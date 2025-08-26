"""
main.py: Gino game.
"""
import pygame
import os
import random

pygame.init()

# Constants
FPS = 60

# Colors
WHITE = (255, 255, 255)

# Dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 720, 400

# Setup
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Gino")

# Images
HORIZON = pygame.transform.scale(pygame.image.load(os.path.join(
    'Assets', 'sprites', 'Horizon.png')), (SCREEN_WIDTH - 10, 10)).convert_alpha()
# CLOUD = pygame.image.load(os.path.join(
#     'Assets', 'sprites', 'Cloud.png')).convert_alpha()

horizon_width = HORIZON.get_width()

tiles = 2
scroll_x = 0


def draw_window():
    """Handles repainting of screen surface
    """
    global scroll_x

    WINDOW.fill(WHITE)
    for i in range(0, tiles):
        WINDOW.blit(HORIZON, (i * horizon_width + scroll_x, SCREEN_HEIGHT//2))

    scroll_x -= 1

    if abs(scroll_x) > horizon_width:
        scroll_x = 0


def main():
    """main code for the game.
    """
    game_running = True
    clock = pygame.time.Clock()

    while game_running:
        clock.tick(FPS)
        # Poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
        draw_window()
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
