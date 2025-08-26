"""
environment.py: controls the rendering and manipulation of the game environment
"""
import pygame
import os
import random

from math import fabs

HORIZON = pygame.image.load(os.path.join(
    'Assets', 'sprites', 'Horizon.png'))
CLOUD = pygame.image.load(os.path.join(
    'Assets', 'sprites', 'Cloud.png'))


class Environment:
    """Wrapper class for handling the environment."""

    def __init__(self, screen_width, screen_height, c_width, c_height):
        self.horizon_tiles = 3
        self.horizon_height = 10
        self.horizon_velocity = 1.2
        self.cloud_velocity = 0.5
        self.horizon_y_pos = screen_height//2 + screen_height//8

        self.screen_width = screen_width
        self.cloud_width = c_width
        self.cloud_height = c_height

        self.horizon_offset_x = 0
        self.cloud_offset_x = 0

        self.cloud_asset = self._scale_asset_image(
            CLOUD, self.cloud_width, self.cloud_height)
        self.horizon_asset = self._scale_asset_image(
            HORIZON, self.screen_width, self.horizon_height)

        self.clouds = []
        self._generate_clouds()

    def _scale_asset_image(self, image, width, height):
        return pygame.transform.scale(image, (width, height)).convert_alpha()

    def _generate_clouds(self):
        """Generate initial or additional clouds"""
        if len(self.clouds) == 0:  # If no clouds yet
            cloud_start = 0
        else:
            cloud_start = self.clouds[-1].x + random.randint(100, 300)

        cloud_y = random.randint(15, 45)
        self.clouds = self.clouds[1:]  # Trim out the first cloud

        self.clouds.extend([pygame.Rect(cloud_start + (i+1) * 200, cloud_y,
                           self.cloud_width, self.cloud_height) for i in range(random.randint(1, 3))])

    def draw_horizon(self, screen):
        """Display horizon on screen"""
        for i in range(self.horizon_tiles):
            screen.blit(self.horizon_asset, (i * self.horizon_asset.get_width() +
                        self.horizon_offset_x, self.horizon_y_pos))

        if fabs(self.horizon_offset_x) > self.horizon_asset.get_width():
            self.horizon_offset_x = 0

    def draw_clouds(self, screen):
        """Display clouds on screen"""
        for cloud in self.clouds:
            screen.blit(self.cloud_asset, (cloud.x +
                        self.cloud_offset_x, cloud.y))

        # If the first cloud is off the screen, generate more
        if (self.clouds[0].x + self.cloud_offset_x + self.cloud_width) < 0:
            self._generate_clouds()

    def animate(self):
        """Animate environment on screen"""
        self.horizon_offset_x -= self.horizon_velocity
        self.cloud_offset_x -= self.cloud_velocity
