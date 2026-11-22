import pygame

from circleshape import CircleShape
from constants import LINE_WIDTH


class Shot(CircleShape):
    def __init__(self: "Shot", *groups) -> None:
        super().__init__(*groups)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", self.rect.center, self.radius, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.rect=self.rect.move((self.velocity*dt).x,(self.velocity*dt).y)
