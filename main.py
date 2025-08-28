"""
main.py: Gino game.
"""
import pygame
import os

pygame.init()

# Constants
FPS = 60
HORIZON_VEL = 0.8
SCREEN_WIDTH, SCREEN_HEIGHT = 720, 400
WHITE = (255, 255, 255)

WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption("Gino")

# Fetch the image
HORIZON = pygame.image.load(os.path.join('Assets', 'sprites', 'Horizon.png'))
HORIZON_Y_POS = SCREEN_HEIGHT//2 + SCREEN_HEIGHT//6


# Global variables
offset_x = 0


def draw_window():
    global offset_x
    horizon_tiles = 2
    horizon_width = HORIZON.get_width()

    WINDOW.fill(WHITE)  # White

    for i in range(horizon_tiles):
        WINDOW.blit(HORIZON, (horizon_width * i + offset_x, HORIZON_Y_POS))

    offset_x -= HORIZON_VEL
    if abs(offset_x) > SCREEN_WIDTH + 100:
        offset_x = 0


def main():
    """main code for the game.
    """
    global offset_x

    game_running = True

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
