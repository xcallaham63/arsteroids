import random

import pygame

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, LINE_WIDTH
from logger import log_event


class Asteroid(CircleShape):
    def __init__(self, *groups) -> None:
        super().__init__(*groups)

        self.rotation=0

        self.mask=pygame.mask.Mask((0,0))
        self.mask_surface=pygame.Surface((0,0), pygame.SRCALPHA)

    def draw(self, screen: pygame.Surface) -> None:
        # debug for visually testing the collision mask
        # screen.blit(self.mask_surface, self.rect)
        pygame.draw.circle(screen, "white", self.rect.center, self.radius, LINE_WIDTH)

    def set_attrs(self, x: float, y: float, radius: float) -> None:
        super().set_attrs(x,y,radius)

        self.set_hit_mask()

    def set_hit_mask(self):
        self.mask_surface=pygame.Surface((self.radius*2,self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(self.mask_surface, "red", (self.radius,self.radius), self.radius, LINE_WIDTH*3)
        self.mask=pygame.mask.from_surface(self.mask_surface)

    def update(self, dt: float) -> None:
        self.rect=self.rect.move((self.velocity*dt).x,(self.velocity*dt).y)

    def split(self) -> None:
        self.kill()
        if self.radius<=ASTEROID_MIN_RADIUS:
            return
        angle=random.uniform(20,50)
        new_radius=self.radius-ASTEROID_MIN_RADIUS
        ast_a=Asteroid()
        ast_a.set_attrs(self.rect.center[0], self.rect.center[1], new_radius)
        ast_a.velocity=self.velocity.rotate(angle)*1.2
        ast_b=Asteroid()
        ast_b.set_attrs(self.rect.center[0], self.rect.center[1], new_radius)
        ast_b.velocity=self.velocity.rotate(0-angle)*1.2
        log_event("asteroid_split",details=f"old velocity: {self.velocity}, new velocities: {ast_a.velocity} {ast_b.velocity}")
