"""
main.py: Gino game.
"""
import pygame
import os
import random

pygame.init()

# Constants
FPS = 60
HORIZON_VEL = 3.0
SCREEN_WIDTH, SCREEN_HEIGHT = 720, 400
DINO_WIDTH, DINO_HEIGHT = 80, 80
JUMP_PACE, FALL_PACE = 25, 5
MAX_JUMP_HEIGHT = 10
WHITE = (255, 255, 255)

WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption("Gino")

# Fetch the images
HORIZON = pygame.image.load(os.path.join('Assets', 'sprites', 'Horizon.png'))
HORIZON_Y_POS = SCREEN_HEIGHT//2 + SCREEN_HEIGHT//4

DINO_STANDING = pygame.transform.scale(pygame.image.load(os.path.join(
    'Assets', 'sprites', 'Dino_Standing.png')), (DINO_WIDTH, DINO_HEIGHT))
DINO_LEFT = pygame.transform.scale(pygame.image.load(os.path.join(
    'Assets', 'sprites', 'Dino_Left_Run.png')), (DINO_WIDTH, DINO_HEIGHT))
DINO_RIGHT = pygame.transform.scale(pygame.image.load(os.path.join(
    'Assets', 'sprites', 'Dino_Right_Run.png')), (DINO_WIDTH, DINO_HEIGHT))

CACTUS = pygame.image.load(os.path.join(
    'Assets', 'sprites', '1_Cactus.png')).convert_alpha()

DINO_X_POS = 30
DINO_Y_POS = HORIZON_Y_POS - DINO_HEIGHT + DINO_HEIGHT//4

# User Events
SWITCH_FOOT = pygame.USEREVENT + 1


# Global variables
offset_x = 0
offset_y = 0
left_foot = True
dino_falling = False
dino_jumping = False

# Timer to switch foot
pygame.time.set_timer(SWITCH_FOOT, 125)


def draw_window(play, dino, obstacles):
    global offset_x, offset_y, dino_jumping
    global left_foot

    horizon_tiles = 2
    horizon_width = HORIZON.get_width()

    WINDOW.fill(WHITE)  # White

    for i in range(horizon_tiles):
        WINDOW.blit(HORIZON, (horizon_width * i + offset_x, HORIZON_Y_POS))

    # Displaying the obstacles
    for obstacle in obstacles:
        cactus_image = pygame.transform.scale(
            CACTUS, (obstacle.width, obstacle.height)).convert_alpha()
        WINDOW.blit(cactus_image, (obstacle.x, obstacle.y))

    if play:
        if dino_jumping:
            # Don't move legs
            WINDOW.blit(DINO_STANDING, (dino.x, dino.y - offset_y))
        else:
            # Move legs
            if left_foot:
                WINDOW.blit(DINO_LEFT, (dino.x, dino.y - offset_y))
            else:
                WINDOW.blit(DINO_RIGHT, (dino.x, dino.y - offset_y))

        offset_x -= HORIZON_VEL
        if abs(offset_x) > SCREEN_WIDTH + 100:
            offset_x = 0
    else:
        WINDOW.blit(DINO_STANDING, (dino.x, dino.y - offset_y))

    pygame.display.update()


def main():
    """main code for the game.
    """
    global offset_y, dino_falling, dino_jumping
    global left_foot

    game_running = True
    play = False

    # Help us manage Dino's position dynamically
    dino = pygame.Rect(DINO_X_POS, DINO_Y_POS, DINO_WIDTH, DINO_HEIGHT)

    # Generate a random number of cacti as initial obstacles
    cacti = []

    num_cactus = random.randint(1, 3)
    cactus_height = random.randint(50, 80)
    for i in range(num_cactus):
        cactus_y_pos = HORIZON_Y_POS - cactus_height + cactus_height//4
        cactus_x_pos = SCREEN_WIDTH - 100 + i*40

        cacti.append(pygame.Rect(
            cactus_x_pos, cactus_y_pos, 40, cactus_height))

    while game_running:

        # Poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

            # Start playing game when SPACE pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                play = True

        while play:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running, play = False, False

                if event.type == SWITCH_FOOT:
                    left_foot = not left_foot

                # FIXME: experimental feature: testing pause functionality
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        play = False

                    # if event.key == pygame.K_SPACE:
                    #     print("jump")

            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE] and not dino_falling:
                # dino.y -= 10  # go up little by little
                # draw_window(play, dino=dino)
                # pygame.display.update()

                dino_jumping = True  # Indicate that Dino is actually jumping

                # If we're not yet at max height, keep going up
                if (dino.y - offset_y) > MAX_JUMP_HEIGHT:
                    offset_y += JUMP_PACE
                else:
                    # Stop going up and wait for 20 milliseconds
                    pygame.time.delay(20)
                    dino_falling = True

            if (dino.y - offset_y) < DINO_Y_POS:
                offset_y -= FALL_PACE

                # Stop dino_falling if we're already on the ground
                if (dino.y - offset_y) >= DINO_Y_POS:
                    dino_falling = False
                    dino_jumping = False  # Dino is no longer jumping

            draw_window(play, dino=dino, obstacles=cacti)

        draw_window(play, dino=dino, obstacles=cacti)

    pygame.quit()


if __name__ == '__main__':
    main()
