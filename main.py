"""
main.py: Gino game.
"""
import pygame
import os
import random

pygame.init()

JUMP_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'tracks', 'jump.wav'))
DIE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'tracks', 'die.wav'))
POINT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'tracks', 'point.wav'))


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
            # Generate a new set of obstacles:
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

        # print((self.clouds[0].x + self.cloud_offset_x))

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


# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# User Events
SWITCH_FOOT = pygame.USEREVENT + 1
COLLISION_DETECTED = pygame.USEREVENT + 2


# Timer to switch foot
pygame.time.set_timer(SWITCH_FOOT, 125)


# TODO: Clean up code base
class GameController:

    def __init__(self):
        self.screen_width = 720
        self.screen_height = 400

        self.window = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        pygame.display.set_caption("Gino")

        self.running = True
        self.is_playing = False
        # self.paused = False
        self.game_over = False

        self.clock = pygame.time.Clock()

        self.score = 0
        self.highscore = 0

        self.score_font = pygame.font.Font(os.path.join(
            'Assets', 'fonts', 'PressStart2P.ttf'), 15)
        self.game_over_font = pygame.font.Font(os.path.join(
            'Assets', 'fonts', 'PressStart2P.ttf'), 30)
        self.game_over_instr_font = pygame.font.Font(os.path.join(
            'Assets', 'fonts', 'PressStart2P.ttf'), 11)
        self.score_x = self.screen_width - 100
        # self.score_y = 20

        self.environment = Environment(
            screen_height=self.screen_height, screen_width=self.screen_width)
        self.dino = Dino(screen_height=self.screen_height)

    def _display_score(self) -> None:
        if self.highscore > 0:
            score_text = f'HI {self.highscore:05} {self.score:05}'
        else:
            score_text = f'{self.score:05}'

        img = self.score_font.render(score_text, True, BLACK)
        self.window.blit(img, (self.score_x, 20))

    def _display_game_over(self) -> None:
        center_y = self.screen_height//2
        center_x = self.screen_width//2

        game_over = self.game_over_font.render("GAME OVER", True, BLACK)
        instruction = self.game_over_instr_font.render(
            "Hit SPACE key to restart", True, BLACK)

        self.window.blit(game_over, (center_x - game_over.get_width() //
                         2, center_y - game_over.get_height()))
        self.window.blit(
            instruction, (center_x - instruction.get_width()//2, center_y))

    def draw(self) -> None:
        self.window.fill(WHITE)

        self.environment.draw_horizon(screen=self.window)
        self.environment.draw_cacti(screen=self.window)
        self.environment.draw_clouds(screen=self.window)

        self.environment.detect_collision(self.dino.rect)

        self._display_score()

        if self.is_playing:
            self.dino.update(screen=self.window)
            self.environment.update()

        else:
            self.dino.draw(screen=self.window)

            if self.game_over:
                self._display_game_over()

        pygame.display.update()

    def play(self) -> None:
        while self.is_playing:
            self.clock.tick(60)   # 60 fps
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running, self.is_playing = False, False

                if event.type == SWITCH_FOOT:
                    # left_foot = not left_foot
                    self.dino.switch_foot()

                    # After every meter run, increment score
                    # A meter run is determined by whether the Dino has extended both legs
                    if self.dino.left_foot:
                        self.score += 1

                    # After every 100 points earned, play Point sound.
                    if self.score % 100 == 0:
                        pygame.mixer.Sound.play(POINT_SOUND)

                # Fires when collision is detected, The game pauses
                if event.type == COLLISION_DETECTED:
                    # Play die sound
                    pygame.mixer.Sound.play(DIE_SOUND)

                    self.is_playing = False
                    self.game_over = True
                    # self.paused = True

                    # Determine if we have a high score or not.
                    if self.score > self.highscore:
                        self.highscore = self.score

                        # Ensures that the score fits the screen
                        self.score_x = self.screen_width - 230

            self.draw()

    def run(self) -> None:
        while self.running:
            # Poll for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Start playing game when SPACE pressed
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:

                    # If we're restarting, clear away obstacles from path

                    self.environment.reset()
                    # # self.dino.reset()
                    self.score = 0
                    self.game_over = False
                    self.is_playing = True

            self.play()
            self.draw()

        pygame.quit()


if __name__ == '__main__':
    game = GameController()
    game.run()
