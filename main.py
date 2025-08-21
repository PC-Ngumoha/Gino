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
    'Assets', 'sprites', 'Horizon.png')), (SCREEN_WIDTH - 0, 10)).convert_alpha()
CLOUD = pygame.transform.scale(pygame.image.load(os.path.join(
    'Assets', 'sprites', 'Cloud.png')), (50, 25)).convert_alpha()

horizon_width = HORIZON.get_width()
cloud_width = CLOUD.get_width()
scroll_x = 0
num_clouds = random.randint(1, 2)


def draw_window():
    """Handles repainting of screen surface
    """
    global scroll_x
    global num_clouds

    horizon_tiles = 2

    horizon_x = (scroll_x * 0.8)
    cloud_x = (scroll_x * 0.4)

    WINDOW.fill(WHITE)

    WINDOW.blit(CLOUD, (100 + cloud_x, 20))

    # Render parallax horizon
    for i in range(0, horizon_tiles):
        WINDOW.blit(HORIZON, (i * horizon_width + horizon_x, SCREEN_HEIGHT//2))

    scroll_x -= 1

    if abs(scroll_x) > horizon_width:
        scroll_x = 0
        # num_clouds = random.randint(1, 2)

    # if abs(cloud_x) > cloud_width:
    #     cloud_x %= cloud_width


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
