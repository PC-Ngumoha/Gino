"""
main.py: Gino game.
"""
import pygame
import os
import random

pygame.init()


class Dino:
    """Dino class"""

    def __init__(self, screen_height: int):
        self.width = 80
        self.height = 80
        self.jump_pace = 25
        self.fall_pace = 5
        self.jumping = False
        self.falling = False
        self.left_foot = True
        self.offset_y = 0
        self.max_height = 10

        self.x = 30
        self.y = screen_height//2 + screen_height//4 - self.height + self.height//4
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.standing_sprite = pygame.transform.scale(pygame.image.load(os.path.join(
            'Assets', 'sprites', 'Dino_Standing.png')), (self.width, self.height))
        self.left_foot_sprite = pygame.transform.scale(pygame.image.load(os.path.join(
            'Assets', 'sprites', 'Dino_Left_Run.png')), (self.width, self.height))
        self.right_foot_sprite = pygame.transform.scale(pygame.image.load(os.path.join(
            'Assets', 'sprites', 'Dino_Right_Run.png')), (self.width, self.height))

    def update(self, screen: pygame.Surface) -> None:
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

        self._update_rect()  # Update position of bounding box

    def _update_rect(self) -> None:
        """Update the position of the bounding box"""
        self.rect.x = self.x
        self.rect.y = self.y - self.offset_y

    def draw(self, screen: pygame.Surface) -> None:
        """Draws Dino before game play starts."""
        screen.blit(self.standing_sprite, (self.x, self.y - self.offset_y))

    def switch_foot(self):
        """Trigger a change in sprite between left_foot and right foot"""
        self.left_foot = not self.left_foot


# TODO: Refactor Environment into seperate class
class Environment:
    """Wrapper class for the game environment"""

    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width

        self.horizon_vel = 4.5
        self.horizon_tiles = 2
        self.horizon_offset_x = 0

        self.horizon_sprite = pygame.image.load(
            os.path.join('Assets', 'sprites', 'Horizon.png'))
        self.horizon_y = screen_height//2 + screen_height//4
        self.horizon_width = self.horizon_sprite.get_width()

        self.cactus_width = 30
        self.cactus_offset_x = 0
        self.cacti = []

        self.cactus_sprite = pygame.image.load(os.path.join(
            'Assets', 'sprites', '1_Cactus.png'))

        self._generate_cacti()

    def draw_horizon(self, screen: pygame.Surface) -> None:
        """draw horizon"""
        for i in range(self.horizon_tiles):
            WINDOW.blit(self.horizon_sprite, (self.horizon_width * i +
                        self.horizon_offset_x, self.horizon_y))

    def draw_cacti(self, screen: pygame.Surface) -> None:
        """draw cacti"""
        # Displaying the obstacles
        for cactus in self.cacti:
            cactus_image = pygame.transform.scale(
                self.cactus_sprite, (cactus.width, cactus.height)).convert_alpha()
            screen.blit(cactus_image, (cactus.x +
                        self.cactus_offset_x, cactus.y))

        # Determine: If right-most cactus in set is completely off the left edge
        if (self.cacti[-1].x + self.cactus_offset_x) < 0:
            # Generate a new set of obstacles:
            self._generate_cacti()

    def detect_collision(self, dino_rect: pygame.Rect) -> None:
        """Detect collision with dino"""
        for cactus in self.cacti:
            # Temporarily shift cactus rect
            moved_rect = cactus.move(self.cactus_offset_x, 0)
            if dino_rect.colliderect(moved_rect):
                pygame.event.post(pygame.event.Event(COLLISION_DETECTED))

    def update(self) -> None:
        """animate environment elements"""
        self.horizon_offset_x -= self.horizon_vel
        self.cactus_offset_x -= self.horizon_vel

        if abs(self.horizon_offset_x) > self.screen_width + 100:
            self.horizon_offset_x = 0

    def _generate_cacti(self) -> None:
        """Utility function: generate new set of obstacles"""
        starting_point = 0
        if len(self.cacti) > 0:
            starting_point = self.cacti[-1].x
            self.cacti.clear()

        num_cactus = random.randint(1, 3)
        cactus_height = random.randint(50, 80)
        for i in range(num_cactus):
            cactus_y = self.horizon_y - cactus_height + cactus_height//4
            cactus_x = starting_point + self.screen_width + \
                i*(self.cactus_width - 10)

            self.cacti.append(pygame.Rect(
                cactus_x, cactus_y, self.cactus_width, cactus_height))


# TODO: Clean up code base

# Constants
FPS = 60
SCREEN_WIDTH, SCREEN_HEIGHT = 720, 400
WHITE = (255, 255, 255)

WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption("Gino")

# User Events
SWITCH_FOOT = pygame.USEREVENT + 1
COLLISION_DETECTED = pygame.USEREVENT + 2


# Timer to switch foot
pygame.time.set_timer(SWITCH_FOOT, 125)


def draw_window(play: bool, dino: Dino, environment: Environment) -> None:

    WINDOW.fill(WHITE)  # White

    environment.detect_collision(dino.rect)

    environment.draw_horizon(screen=WINDOW)
    environment.draw_cacti(screen=WINDOW)

    if play:

        dino.update(screen=WINDOW)
        environment.update()
    else:
        dino.draw(screen=WINDOW)

    pygame.display.update()


def main() -> None:
    """main code for the game.
    """
    game_running = True
    play = False

    dino = Dino(screen_height=SCREEN_HEIGHT)

    environment = Environment(
        screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT)

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

                # Fires when collision is detected, The game pauses
                if event.type == COLLISION_DETECTED:
                    play = False

            draw_window(play, dino=dino, environment=environment)

        draw_window(play, dino=dino, environment=environment)

    pygame.quit()


if __name__ == '__main__':
    main()
