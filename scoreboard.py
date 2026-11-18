import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from gamestate import GameState


class Scoreboard(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self: "Scoreboard", gamestate: GameState) -> None:
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()
        self.font_size=SCREEN_HEIGHT/25

        self.gamestate=gamestate
        self.font=pygame.font.Font(None, int(self.font_size))

    def draw(self: "Scoreboard", screen: pygame.Surface) -> None:
        self.image=pygame.Surface((self.score_image.get_width(),self.font_size*2+5))
        self.image.blit(self.score_image, (0,0))
        self.image.blit(self.lives_image, (0,self.font_size+5))
        self.rect=self.image.get_rect(midtop=(SCREEN_WIDTH/2, 0))
        screen.blit(self.image,self.rect)

    def update(self: "Scoreboard", dt: float) -> None:

        self.score_image=self.font.render(f"Score: {self.gamestate.score}", True, "White")
        self.lives_image=self.font.render(f"Lives: {self.gamestate.lives}", True, "White")
