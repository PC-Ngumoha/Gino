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
OBSTACLE_Y_POS = SCREEN_HEIGHT//2 + SCREEN_HEIGHT//8 - OBSTACLE_HEIGHT + 15
OBSTACLE_DISTANCES = (50, 75, 100)

pygame.display.set_caption("Gino")

# Images
ONE_CACTUS = pygame.transform.scale(pygame.image.load(os.path.join(
    'Assets', 'sprites', '1_Cactus.png')), (OBSTACLE_WIDTH, OBSTACLE_HEIGHT)).convert_alpha()


# Events
SWITCH_FOOT = pygame.USEREVENT + 1
ADD_OBSTACLES = pygame.USEREVENT + 2

# Timers
pygame.time.set_timer(SWITCH_FOOT, 125)

obstacle_scroll_x = 0
left_foot = True


def draw_window(dino, environment, obstacles, play=True):
    """Handles repainting of screen surface
    """
    global obstacle_scroll_x
    global left_foot

    WINDOW.fill(WHITE)

    environment.draw_clouds(WINDOW)

    environment.draw_horizon(WINDOW)

    # Render obstacles on path
    for obstacle in obstacles:
        WINDOW.blit(ONE_CACTUS, (obstacle.x + obstacle_scroll_x, obstacle.y))

    # Raise ADD_OBSTACLES event when the last of the obstacles goes off screen
    if (obstacles[-1].x + obstacle_scroll_x + 100) < 0:
        pygame.event.post(pygame.event.Event(ADD_OBSTACLES))

    # Normal game play if ON, static image if OFF
    if play:
        dino.move(left_foot)
        environment.animate()

        obstacle_scroll_x -= HORIZON_VEL

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
        SCREEN_WIDTH, SCREEN_HEIGHT, CLOUD_WIDTH, CLOUD_HEIGHT)

    # Generate random number of obstacles to be placed on the road
    obstacles = [pygame.Rect(SCREEN_WIDTH + 10 + i*50, OBSTACLE_Y_POS, OBSTACLE_WIDTH,
                             OBSTACLE_HEIGHT) for i in range(random.randint(1, 3)) for i in range(random.randint(1, 3))]

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

                # Handling the event to add obstacles to path
                if event.type == ADD_OBSTACLES:
                    obstacle_x = obstacles[-1].x + (SCREEN_WIDTH + 100)

                    obstacles.clear()  # Clear previous obstacles

                    obstacles.extend([pygame.Rect(obstacle_x + i*50, OBSTACLE_Y_POS,
                                     OBSTACLE_WIDTH, OBSTACLE_HEIGHT) for i in range(random.randint(1, 3))])

            # keys = pygame.key.get_pressed()
            # if keys[pygame.K_SPACE]:
            #     print("Jump")

            # Draw window for subsequent screen.
            draw_window(dino, environment, obstacles)

        draw_window(dino, environment, obstacles, play)  # Draw initial screen.

    pygame.quit()


if __name__ == '__main__':
    main()
