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
DINO_WIDTH, DINO_HEIGHT = 80, 80
WHITE = (255, 255, 255)

WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption("Gino")

# Fetch the images
HORIZON = pygame.image.load(os.path.join('Assets', 'sprites', 'Horizon.png'))
HORIZON_Y_POS = SCREEN_HEIGHT//2 + SCREEN_HEIGHT//6

DINO_STANDING = pygame.transform.scale(pygame.image.load(os.path.join(
    'Assets', 'sprites', 'Dino_Standing.png')), (DINO_WIDTH, DINO_HEIGHT))
DINO_LEFT = pygame.transform.scale(pygame.image.load(os.path.join(
    'Assets', 'sprites', 'Dino_Left_Run.png')), (DINO_WIDTH, DINO_HEIGHT))
DINO_RIGHT = pygame.transform.scale(pygame.image.load(os.path.join(
    'Assets', 'sprites', 'Dino_Right_Run.png')), (DINO_WIDTH, DINO_HEIGHT))

DINO_X_POS = 30
DINO_Y_POS = HORIZON_Y_POS - DINO_HEIGHT + DINO_HEIGHT//4

# User Events
SWITCH_FOOT = pygame.USEREVENT + 1


# Global variables
offset_x = 0
offset_y = 0
left_foot = True
dino_falling = False

# Timer to switch foot
pygame.time.set_timer(SWITCH_FOOT, 125)


def draw_window(play, dino):
    global offset_x, offset_y
    global left_foot

    horizon_tiles = 2
    horizon_width = HORIZON.get_width()

    WINDOW.fill(WHITE)  # White

    for i in range(horizon_tiles):
        WINDOW.blit(HORIZON, (horizon_width * i + offset_x, HORIZON_Y_POS))

    if play:
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
    global offset_y, dino_falling
    global left_foot

    game_running = True
    play = False

    # Help us manage Dino's position dynamically
    dino = pygame.Rect(DINO_X_POS, DINO_Y_POS, DINO_WIDTH, DINO_HEIGHT)

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

                # If we're not yet at max height, keep going up
                if (dino.y - offset_y) > 30:
                    offset_y += 10
                else:
                    # Stop going up and wait for 20 milliseconds
                    pygame.time.wait(100)
                    dino_falling = True

            if (dino.y - offset_y) < DINO_Y_POS or dino_falling:
                offset_y -= 3

                # Stop dino_falling if we're already on the ground
                if (dino.y - offset_y) >= DINO_Y_POS and dino_falling:
                    dino_falling = False

            draw_window(play, dino=dino)

        draw_window(play, dino=dino)

    pygame.quit()


if __name__ == '__main__':
    main()
