"""
constants.py: Contains all constants needed for game functionality
"""
import pygame
import os

pygame.mixer.init()

# Sounds
JUMP_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'tracks', 'jump.wav'))
DIE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'tracks', 'die.wav'))
POINT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'tracks', 'point.wav'))

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# User Events
SWITCH_FOOT = pygame.USEREVENT + 1
COLLISION_DETECTED = pygame.USEREVENT + 2
