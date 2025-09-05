"""
main.py: Gino game.
"""
import pygame
import os

from dino import Dino
from environment import Environment

from constants import WHITE, BLACK, SWITCH_FOOT, COLLISION_DETECTED, POINT_SOUND, DIE_SOUND

pygame.init()


# Timer to switch foot
pygame.time.set_timer(SWITCH_FOOT, 125)


class GameController:

    def __init__(self):
        self.screen_width = 720
        self.screen_height = 400

        self.window = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        pygame.display.set_caption("Gino")

        self.running = True
        self.is_playing = False
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
                    self.dino.switch_foot()

                    # After every meter run, increment score
                    # A meter run is determined by whether the Dino has extended both legs
                    if self.dino.left_foot:
                        self.score += 1

                    # After every 100 points earned, play Point sound then run faster
                    if self.score % 100 == 0:
                        pygame.mixer.Sound.play(POINT_SOUND)
                        self.environment.move_faster()

                # Fires when collision is detected, The game pauses
                if event.type == COLLISION_DETECTED:
                    # Play die sound
                    pygame.mixer.Sound.play(DIE_SOUND)

                    self.is_playing = False
                    self.game_over = True

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
                    self.score = 0
                    self.game_over = False
                    self.is_playing = True

            self.play()
            self.draw()

        pygame.quit()


if __name__ == '__main__':
    game = GameController()
    game.run()
