"""
environment.py: Contains code for controlling game environment
"""
import pygame
import os
import random

from constants import COLLISION_DETECTED


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

        self.cloud_width = 55
        self.cloud_height = 30
        self.cloud_vel = 0.2
        self.cloud_offset_x = 0
        self.clouds = []

        self.cactus_sprite = pygame.image.load(os.path.join(
            'Assets', 'sprites', '1_Cactus.png'))
        self.cloud_sprite = pygame.transform.scale(pygame.image.load(os.path.join(
            'Assets', 'sprites', 'Cloud.png')), (self.cloud_width, self.cloud_height))

        self._generate_cacti()
        self._generate_clouds()

    def draw_horizon(self, screen: pygame.Surface) -> None:
        """draw horizon"""
        for i in range(self.horizon_tiles):
            screen.blit(self.horizon_sprite, (self.horizon_width * i +
                        self.horizon_offset_x, self.horizon_y))

    def draw_cacti(self, screen: pygame.Surface) -> None:
        """Draw cacti"""
        # Displaying the obstacles
        for cactus in self.cacti:
            cactus_image = pygame.transform.scale(
                self.cactus_sprite, (cactus.width, cactus.height)).convert_alpha()
            screen.blit(cactus_image, (cactus.x +
                        self.cactus_offset_x, cactus.y))

        # Determine: If right-most cactus in set is completely off the left edge
        if (self.cacti[-1].x + self.cactus_offset_x) < 0:
            self._generate_cacti()

    def draw_clouds(self, screen: pygame.Surface) -> None:
        """Draw clouds"""
        for cloud in self.clouds:
            screen.blit(self.cloud_sprite, (cloud.x +
                        self.cloud_offset_x, cloud.y))

        # When the first cloud goes off left edge, generate new set of clouds
        if len(self.clouds) > 0:
            if (self.clouds[0].x + self.cloud_offset_x + 50) < 0:
                self._generate_clouds()
        else:
            self._generate_clouds()

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
        self.cloud_offset_x -= self.cloud_vel

        if abs(self.horizon_offset_x) > self.screen_width + 100:
            self.horizon_offset_x = 0

    def reset(self) -> None:
        """Reset the state of the environment"""
        self.cacti.clear()
        self._generate_cacti()

        self.horizon_offset_x = 0
        self.cactus_offset_x = 0

    def move_faster(self) -> None:
        """Cause environment to move a little bit faster"""
        self.horizon_vel += 0.1

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

    def _generate_clouds(self) -> None:
        starting_point = 100
        if len(self.clouds) > 0:
            starting_point = self.clouds[-1].x
            self.clouds = self.clouds[1:]

        num_clouds = random.randint(0, 3)
        self.clouds.extend([pygame.Rect(starting_point + (i+1)*150, (i+1)*20,
                           self.cloud_width, self.cloud_height) for i in range(num_clouds)])
