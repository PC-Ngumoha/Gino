"""
main.py: Gino game.
"""
import pygame

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


def draw_window(dino, environment, play=True):
    """Handles repainting of screen surface
    """
    WINDOW.fill(WHITE)

    environment.draw_clouds(screen=WINDOW)

    environment.draw_horizon(screen=WINDOW)

    environment.draw_obstacles(screen=WINDOW)

    # Normal game play if ON, static image if OFF
    if play:
        dino.move()
        environment.animate()
    else:
        dino.stand()

    dino.update(screen=WINDOW)
    pygame.display.update()


def main():
    """main code for the game.
    """

    game_running = True
    play = False
    clock = pygame.time.Clock()

    dino = Dino(x=DINO_X_POS, y=DINO_Y_POS,
                width=DINO_WIDTH, height=DINO_HEIGHT)
    environment = Environment(
        screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT,
        c_width=CLOUD_WIDTH, c_height=CLOUD_HEIGHT,
        o_width=OBSTACLE_WIDTH, o_height=OBSTACLE_HEIGHT)

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
                    dino.switch_foot()  # Invert left_foot

            # Draw window for subsequent screen.
            draw_window(dino, environment)

        draw_window(dino, environment, play)  # Draw initial screen.

    pygame.quit()


if __name__ == '__main__':
    main()
