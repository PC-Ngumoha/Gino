"""
main.py: Gino game.
"""
import pygame
import os
import random

pygame.init()

# TODO: Refactor Dino into seperate class


class Dino:

    def __init__(self, screen_height):
        self.width = 80
        self.height = 80
        self.jump_pace = 25
        self.fall_pace = 6
        self.jumping = False
        self.falling = False
        self.left_foot = True
        self.offset_y = 0
        self.max_height = 10

        self.x = 30
        self.y = screen_height//2 + screen_height//4 - self.height + self.height//4

        self.standing_sprite = pygame.transform.scale(pygame.image.load(os.path.join(
            'Assets', 'sprites', 'Dino_Standing.png')), (self.width, self.height))
        self.left_foot_sprite = pygame.transform.scale(pygame.image.load(os.path.join(
            'Assets', 'sprites', 'Dino_Left_Run.png')), (self.width, self.height))
        self.right_foot_sprite = pygame.transform.scale(pygame.image.load(os.path.join(
            'Assets', 'sprites', 'Dino_Right_Run.png')), (self.width, self.height))

    def update(self, screen):
        """Handles animating Dino on screen"""
        keys = pygame.key.get_pressed()

        # init jumping when SPACE pressed
        if keys[pygame.K_SPACE] and not self.falling:

            self.jumping = True

            if (self.y - self.offset_y) > self.max_height:
                self.offset_y += self.jump_pace
            else:
                self.falling = True

        # Determine if above ground level
        if (self.y - self.offset_y) < self.y:
            self.offset_y -= self.fall_pace

            # At ground level
            if (self.y - self.offset_y) >= self.y:
                self.jumping = False
                self.falling = False

        if self.jumping:
            # Don't move legs
            screen.blit(self.standing_sprite, (self.x, self.y - self.offset_y))
        else:
            # Move legs
            if self.left_foot:
                screen.blit(self.left_foot_sprite,
                            (self.x, self.y - self.offset_y))
            else:
                screen.blit(self.right_foot_sprite,
                            (self.x, self.y - self.offset_y))

    def draw(self, screen):
        """Draws Dino before game play starts."""
        screen.blit(self.standing_sprite, (self.x, self.y))

    def switch_foot(self):
        """Trigger a change in sprite between left_foot and right foot"""
        self.left_foot = not self.left_foot


# TODO: Refactor Environment into seperate class

# TODO: Clean up code base

# Constants
FPS = 60
HORIZON_VEL = 4.2
SCREEN_WIDTH, SCREEN_HEIGHT = 720, 400
CACTUS_WIDTH = 30
WHITE = (255, 255, 255)

WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption("Gino")

# Fetch the images
HORIZON = pygame.image.load(os.path.join('Assets', 'sprites', 'Horizon.png'))
HORIZON_Y_POS = SCREEN_HEIGHT//2 + SCREEN_HEIGHT//4

CACTUS = pygame.image.load(os.path.join(
    'Assets', 'sprites', '1_Cactus.png')).convert_alpha()

# User Events
SWITCH_FOOT = pygame.USEREVENT + 1
GENERATE_OBSTACLES = pygame.USEREVENT + 2


# Global variables
offset_x = 0
obstacle_offset_x = 0

# Timer to switch foot
pygame.time.set_timer(SWITCH_FOOT, 125)


def draw_window(play, dino, obstacles):
    global offset_x, obstacle_offset_x

    horizon_tiles = 2
    horizon_width = HORIZON.get_width()

    WINDOW.fill(WHITE)  # White

    for i in range(horizon_tiles):
        WINDOW.blit(HORIZON, (horizon_width * i + offset_x, HORIZON_Y_POS))

    # Displaying the obstacles
    for obstacle in obstacles:
        cactus_image = pygame.transform.scale(
            CACTUS, (obstacle.width, obstacle.height)).convert_alpha()
        WINDOW.blit(cactus_image, (obstacle.x + obstacle_offset_x, obstacle.y))

    # Determine: If left-most obstacle is completely off the left edge
    if (obstacles[-1].x + obstacle_offset_x) < 0:
        # Generate a new set of obstacles:
        pygame.event.post(pygame.event.Event(GENERATE_OBSTACLES))

    if play:

        dino.update(screen=WINDOW)

        offset_x -= HORIZON_VEL
        obstacle_offset_x -= HORIZON_VEL

        if abs(offset_x) > SCREEN_WIDTH + 100:
            offset_x = 0
    else:
        dino.draw(screen=WINDOW)

    pygame.display.update()


def generate_cacti(starting_point=0):

    cacti = []

    num_cactus = random.randint(1, 3)
    cactus_height = random.randint(50, 80)
    for i in range(num_cactus):
        cactus_y_pos = HORIZON_Y_POS - cactus_height + cactus_height//4
        cactus_x_pos = starting_point + SCREEN_WIDTH + i*CACTUS_WIDTH

        cacti.append(pygame.Rect(
            cactus_x_pos, cactus_y_pos, CACTUS_WIDTH, cactus_height))

    return cacti


def main():
    """main code for the game.
    """
    game_running = True
    play = False

    dino = Dino(screen_height=SCREEN_HEIGHT)

    # Generate a random number of cacti as initial obstacles
    cacti = generate_cacti()

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
                    # left_foot = not left_foot
                    dino.switch_foot()

                # FIXME: experimental feature: testing pause functionality
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        play = False

                if event.type == GENERATE_OBSTACLES:
                    last_obstacle_x = cacti[-1].x

                    cacti.clear()  # Remove all obstacles in initial set

                    cacti = generate_cacti(starting_point=last_obstacle_x)

            draw_window(play, dino=dino, obstacles=cacti)

        draw_window(play, dino=dino, obstacles=cacti)

    pygame.quit()


if __name__ == '__main__':
    main()
