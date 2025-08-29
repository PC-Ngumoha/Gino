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
DINO_Y_POS = HORIZON_Y_POS - DINO_HEIGHT + DINO_HEIGHT//4

# User Events
SWITCH_FOOT = pygame.USEREVENT + 1


# Global variables
offset_x = 0
left_foot = True

# Timer to switch foot
pygame.time.set_timer(SWITCH_FOOT, 125)


def draw_window(play):
    global offset_x
    global left_foot

    horizon_tiles = 2
    horizon_width = HORIZON.get_width()

    WINDOW.fill(WHITE)  # White

    for i in range(horizon_tiles):
        WINDOW.blit(HORIZON, (horizon_width * i + offset_x, HORIZON_Y_POS))

    if play:
        if left_foot:
            WINDOW.blit(DINO_LEFT, (30, DINO_Y_POS))
        else:
            WINDOW.blit(DINO_RIGHT, (30, DINO_Y_POS))

        offset_x -= HORIZON_VEL
        if abs(offset_x) > SCREEN_WIDTH + 100:
            offset_x = 0
    else:
        WINDOW.blit(DINO_STANDING, (30, DINO_Y_POS))

    pygame.display.update()


def main():
    """main code for the game.
    """
    global left_foot

    game_running = True
    play = False

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

            if keys[pygame.K_SPACE]:
                print('Jump')

            draw_window(play)

        draw_window(play)

    pygame.quit()


if __name__ == '__main__':
    main()
