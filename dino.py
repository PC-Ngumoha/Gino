"""
dino.py: specify Dino attributes and methods.
"""
import pygame
import os

# Sprite Images
DINO_STANDING = pygame.image.load(os.path.join(
    'Assets', 'sprites', 'Dino_Standing.png'))

DINO_LEFT = pygame.image.load(os.path.join(
    'Assets', 'sprites', 'Dino_Left_Run.png'))

DINO_RIGHT = pygame.image.load(os.path.join(
    'Assets', 'sprites', 'Dino_Right_Run.png'))


class Dino:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = self._scale_sprite_image(DINO_STANDING)
        # self.rect = pygame.Rect(x, y, width, height)
        self.left_foot = True

    def update(self, screen):
        """Display changes on screen"""
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        """Create the illusion of foots switching"""
        if self.left_foot:
            self.image = self._scale_sprite_image(DINO_LEFT)
        else:
            self.image = self._scale_sprite_image(DINO_RIGHT)

    def _scale_sprite_image(self, image):
        """Helper method: scales sprite to size"""
        return pygame.transform.scale(image, (self.width, self.height)).convert_alpha()

    def stand(self):
        """Take a standing posture"""
        self.image = self._scale_sprite_image(DINO_STANDING)

    def switch_foot(self):
        """Switch from left to right foot and vice versa."""
        self.left_foot = not self.left_foot

    # def update_rect(self):
    #     self.rect.x = self.x
    #     self.rect.y = self.y
