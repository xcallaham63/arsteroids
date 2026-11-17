import random

import pygame

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH
from logger import log_event


class Asteroid(CircleShape):
    def __init__(self: "Asteroid", x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

        self.rotation=0

    def draw(self: "Asteroid", screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self: "Asteroid", dt: float) -> None:
        self.position+=self.velocity*dt

    def split(self: "Asteroid") -> None:
        self.kill()
        if self.radius<=ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        angle=random.uniform(20,50)
        new_angle_a=self.velocity.rotate(angle)
        new_angle_b=self.velocity.rotate(0-angle)
        new_radius=self.radius-ASTEROID_MIN_RADIUS
        ast_a=Asteroid(self.position.x, self.position.y, new_radius)
        ast_a.velocity=new_angle_a*1.2
        ast_b=Asteroid(self.position.x, self.position.y, new_radius)
        ast_b.velocity=new_angle_b*1.2
