import pygame

from circleshape import CircleShape
from constants import (
    LINE_WIDTH,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
    SHOT_RADIUS,
)
from shot import Shot


class Player(CircleShape):
    def __init__(self: "Player", *groups) -> None:
        super().__init__(*groups)

        self.rotation=0
        self.shoot_timer=0
        self.rect=pygame.Rect(0,0,0,0)
        self.image=pygame.Surface((0,0))
        self.mask_surface=pygame.Surface((0,0))
        self.mask=pygame.mask.from_surface(self.mask_surface)

    def draw(self, screen: pygame.Surface) -> None:
        # screen.blit(self.mask.to_surface(), self.rect)

        offset=self.triangle_offset(pygame.Vector2(self.rect.center[0],self.rect.center[1]))
        pygame.draw.polygon(screen,"white", offset, LINE_WIDTH)

    def move(self, dt: float) -> None:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        moved = forward * PLAYER_SPEED * dt

        self.rect = self.rect.move(moved.x,moved.y)

    def rotate(self, dt: float):
        self.rotation += PLAYER_TURN_SPEED*dt
        self.set_hit_mask()

    def set_attrs(self: "Player", x: float, y: float, radius: float) -> None:
        super().set_attrs(x,y,radius)

        self.set_hit_mask()

    def set_hit_mask(self: "Player"):
        self.mask_surface=pygame.Surface((self.radius*2,self.radius*2), pygame.SRCALPHA)
        pygame.draw.polygon(self.mask_surface, "red", self.triangle_offset(pygame.Vector2(self.radius,self.radius)), LINE_WIDTH)
        self.mask=pygame.mask.from_surface(self.mask_surface)
        # do this after so the gray box isn't part of the hit mask, but will be displayed
        pygame.draw.rect(self.mask_surface, "gray", self.mask_surface.get_rect(), LINE_WIDTH)

    def shoot(self) -> None:
        if self.shoot_timer>0:
            return
        self.shoot_timer=PLAYER_SHOOT_COOLDOWN_SECONDS
        shot=Shot()
        shot.set_attrs(self.rect.center[0], self.rect.center[1], SHOT_RADIUS)
        shot.velocity = pygame.Vector2(0,1).rotate(self.rotation)*PLAYER_SHOOT_SPEED

    def triangle(self) -> list[pygame.Vector2]:
        center=pygame.Vector2(self.rect.center[0],self.rect.center[1])
        # print(f"Player: triangle: centered on: {center}")
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = center + forward * self.radius
        b = center - forward * self.radius - right
        c = center - forward * self.radius + right
        return [a, b, c]

    def triangle_offset(self, center: pygame.Vector2 | None ) -> list[pygame.Vector2]:
        if center==None:
            center=pygame.Vector2(self.rect.center[0], self.rect.center[1])
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = center + forward * self.radius
        b = center - forward * self.radius - right
        c = center - forward * self.radius + right
        return [a, b, c]

    def update(self, dt: float) -> None:
        self.shoot_timer-=dt

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(0-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
