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
HORIZON_VEL = 1.2
CLOUD_VEL = 0.5
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
HORIZON = pygame.transform.scale(pygame.image.load(os.path.join(
    'Assets', 'sprites', 'Horizon.png')), (SCREEN_WIDTH - 0, 10)).convert_alpha()
CLOUD = pygame.transform.scale(pygame.image.load(os.path.join(
    'Assets', 'sprites', 'Cloud.png')), (CLOUD_WIDTH, CLOUD_HEIGHT)).convert_alpha()

DINO_STANDING = pygame.transform.scale(pygame.image.load(os.path.join(
    'Assets', 'sprites', 'Dino_Standing.png')), (DINO_WIDTH, DINO_HEIGHT)).convert_alpha()

DINO_LEFT = pygame.transform.scale(pygame.image.load(os.path.join(
    'Assets', 'sprites', 'Dino_Left_Run.png')), (DINO_WIDTH, DINO_HEIGHT)).convert_alpha()

DINO_RIGHT = pygame.transform.scale(pygame.image.load(os.path.join(
    'Assets', 'sprites', 'Dino_Right_Run.png')), (DINO_WIDTH, DINO_HEIGHT)).convert_alpha()

ONE_CACTUS = pygame.transform.scale(pygame.image.load(os.path.join(
    'Assets', 'sprites', '1_Cactus.png')), (OBSTACLE_WIDTH, OBSTACLE_HEIGHT)).convert_alpha()


# Events
GENERATE_MORE_CLOUDS = pygame.USEREVENT + 1
SWITCH_FOOT = pygame.USEREVENT + 2
ADD_OBSTACLES = pygame.USEREVENT + 3

# Timers
pygame.time.set_timer(SWITCH_FOOT, 125)
# pygame.time.set_timer(ADD_OBSTACLES, 1200)

horizon_width = HORIZON.get_width()
horizon_scroll_x = 0
cloud_scroll_x = 0
obstacle_scroll_x = 0
left_foot = True


def draw_window(dino, clouds, obstacles, play=True):
    """Handles repainting of screen surface
    """
    global horizon_scroll_x
    global obstacle_scroll_x
    global cloud_scroll_x

    horizon_tiles = 3

    WINDOW.fill(WHITE)

    # Render parallax clouds
    for cloud in clouds:
        WINDOW.blit(CLOUD, (cloud.x + cloud_scroll_x, cloud.y))

    # Render parallax horizon
    for i in range(0, horizon_tiles):
        WINDOW.blit(HORIZON, (i * horizon_width +
                    horizon_scroll_x, SCREEN_HEIGHT//2 + SCREEN_HEIGHT//8))

    # Render obstacles on path
    for obstacle in obstacles:
        WINDOW.blit(ONE_CACTUS, (obstacle.x + obstacle_scroll_x, obstacle.y))

    # Raise ADD_OBSTACLES event when the last of the obstacles goes off screen
    if (obstacles[-1].x + obstacle_scroll_x + 100) < 0:
        pygame.event.post(pygame.event.Event(ADD_OBSTACLES))

    # Normal game play if ON, static image if OFF
    if play:
        make_dino_move(dino)

        horizon_scroll_x -= HORIZON_VEL
        obstacle_scroll_x -= HORIZON_VEL
        cloud_scroll_x -= CLOUD_VEL

        if fabs(horizon_scroll_x) > horizon_width:
            pygame.event.post(pygame.event.Event(GENERATE_MORE_CLOUDS))
            horizon_scroll_x = 0

    else:
        # Dino stands
        WINDOW.blit(DINO_STANDING, (dino.x, dino.y))

    pygame.display.update()


def make_dino_move(dino):
    global left_foot

    # Switch between Dino sprites to create illusion of left..right motion.
    if left_foot:
        WINDOW.blit(DINO_LEFT, (dino.x, dino.y))
        # left_foot = False
    else:
        WINDOW.blit(DINO_RIGHT, (dino.x, dino.y))
        # left_foot = True


def main():
    """main code for the game.
    """
    global left_foot

    game_running = True
    play = False
    clock = pygame.time.Clock()

    # Create bounding box for Dino
    dino = pygame.Rect(DINO_X_POS, DINO_Y_POS, DINO_WIDTH, DINO_HEIGHT)

    # Generate a random number of clouds to move in parallax
    clouds = [pygame.Rect((i+1) * 200, (i+1) * 15, CLOUD_WIDTH, CLOUD_HEIGHT)
              for i in range(random.randint(1, 3))]

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

                # Catching and handling generate cloud events
                if event.type == GENERATE_MORE_CLOUDS:
                    # New starting points
                    cloud_x = clouds[-1].x + random.randint(100, 300)
                    cloud_y = random.randint(15, 45)

                    clouds = clouds[1:]  # Shift out the first cloud

                    # Add a new set of clouds at the tailend of the initial set
                    clouds.extend([pygame.Rect(cloud_x + i*200, cloud_y,
                                               CLOUD_WIDTH, CLOUD_HEIGHT) for i in range(random.randint(1, 3))])

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
            draw_window(dino, clouds, obstacles)

        draw_window(dino, clouds, obstacles, play)  # Draw initial screen.

    pygame.quit()


if __name__ == '__main__':
    main()
