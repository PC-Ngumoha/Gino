"""
main.py: Gino game.
"""
import pygame
import os
import random
from math import fabs

# Game Entities import
from dino import Dino
from environment import Environment

pygame.init()

# Constants
FPS = 60
HORIZON_VEL = 1.2
CLOUD_WIDTH, CLOUD_HEIGHT = 50, 25
DINO_WIDTH, DINO_HEIGHT = 70, 80
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 50, 70
MAX_HEIGHT = 150

# Colors
WHITE = (255, 255, 255)

# Dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 720, 400

# Setup
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DINO_X_POS = 30
DINO_Y_POS = SCREEN_HEIGHT//2 + SCREEN_HEIGHT//8 - DINO_HEIGHT + 15

pygame.display.set_caption("Gino")

# Events
SWITCH_FOOT = pygame.USEREVENT + 1

# Timers
pygame.time.set_timer(SWITCH_FOOT, 125)

left_foot = True


def draw_window(dino, environment, play=True):
    """Handles repainting of screen surface
    """
    # global obstacle_scroll_x
    global left_foot

    WINDOW.fill(WHITE)

    environment.draw_clouds(WINDOW)

    environment.draw_horizon(WINDOW)

    environment.draw_obstacles(WINDOW)

    # Normal game play if ON, static image if OFF
    if play:
        dino.move(left_foot)
        environment.animate()
    else:
        dino.stand()

    dino.update(WINDOW)
    pygame.display.update()


def main():
    """main code for the game.
    """
    global left_foot

    game_running = True
    play = False
    clock = pygame.time.Clock()

    dino = Dino(DINO_X_POS, DINO_Y_POS, DINO_WIDTH, DINO_HEIGHT)
    environment = Environment(
        SCREEN_WIDTH, SCREEN_HEIGHT, CLOUD_WIDTH, CLOUD_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)

    while game_running:
        # Poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    play = True

        while play:
            clock.tick(FPS)
            # Poll for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running, play = False, False

                # Testing the pause functionality
                # FIXME: Remove me when game is complete.
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        play = False

                    if event.key == pygame.K_SPACE:
                        print("Jump")

                # Handling the switch between Dino's right and left foot while moving
                if event.type == SWITCH_FOOT:
                    left_foot = not left_foot  # Invert left_foot

            # Draw window for subsequent screen.
            draw_window(dino, environment)

        draw_window(dino, environment, play)  # Draw initial screen.

    pygame.quit()


if __name__ == '__main__':
    main()
