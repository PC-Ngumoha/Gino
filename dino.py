"""
dino.py: Contains all the code for the running Dinosaur
"""
import pygame
import os

from constants import JUMP_SOUND


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

            if not self.jumping:
                # Play jump sound
                pygame.mixer.Sound.play(JUMP_SOUND)

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

    def switch_foot(self) -> None:
        """Trigger a change in sprite between left_foot and right foot"""
        self.left_foot = not self.left_foot

    def reset(self) -> None:
        """Reset the Dinosaur's state"""
        self.offset_y = 0
