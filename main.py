"""
main.py: Gino game.
"""
import pygame
import os
import random
from math import fabs

pygame.init()

# Constants
FPS = 60
CLOUD_WIDTH, CLOUD_HEIGHT = 50, 25

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
    'Assets', 'sprites', 'Cloud.png')), (CLOUD_WIDTH, CLOUD_HEIGHT)).convert_alpha()

# Events
GENERATE_MORE_CLOUDS = pygame.USEREVENT + 1

horizon_width = HORIZON.get_width()
horizon_scroll_x = 0
cloud_scroll_x = 0


def draw_window(clouds):
    """Handles repainting of screen surface
    """
    global horizon_scroll_x
    global cloud_scroll_x

    horizon_tiles = 3

    WINDOW.fill(WHITE)

    # Render parallax clouds
    for cloud in clouds:
        WINDOW.blit(CLOUD, (cloud.x + cloud_scroll_x, cloud.y))

    # Render parallax horizon
    for i in range(0, horizon_tiles):
        WINDOW.blit(HORIZON, (i * horizon_width +
                    horizon_scroll_x, SCREEN_HEIGHT//2))

    horizon_scroll_x -= 0.8
    cloud_scroll_x -= 0.4

    if fabs(horizon_scroll_x) > horizon_width:
        pygame.event.post(pygame.event.Event(GENERATE_MORE_CLOUDS))
        horizon_scroll_x = 0


def main():
    """main code for the game.
    """
    game_running = True
    clock = pygame.time.Clock()

    # Generate a random number of clouds to move in parallax
    clouds = [pygame.Rect((i+1) * 200, (i+1) * 15, CLOUD_WIDTH, CLOUD_HEIGHT)
              for i in range(random.randint(1, 3))]

    while game_running:
        clock.tick(FPS)
        # Poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

            # Catching and handling generate cloud events
            if event.type == GENERATE_MORE_CLOUDS:
                # New starting points
                cloud_x = clouds[-1].x + random.randint(100, 300)
                cloud_y = random.randint(15, 45)

                clouds = clouds[1:]  # Shift out the first cloud

                # Add a new set of clouds at the tailend of the initial set
                clouds.extend([pygame.Rect(cloud_x + i*200, cloud_y,
                              CLOUD_WIDTH, CLOUD_HEIGHT) for i in range(random.randint(1, 3))])

        draw_window(clouds)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
