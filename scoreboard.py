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

        self.gamestate=gamestate

        self.font=pygame.font.Font(None, int(SCREEN_HEIGHT/12))
        self.update(0)
        self.rect=self.image.get_rect(midtop=(SCREEN_WIDTH/2, 0))

    def draw(self: "Scoreboard", screen: pygame.Surface) -> None:
        screen.blit(self.image,self.rect)

    def update(self: "Scoreboard", dt: float) -> None:
        self.image=self.font.render(f"Score: {self.gamestate.score}", True, "White")
