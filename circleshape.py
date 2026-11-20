import pygame


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self: "CircleShape", *groups) -> None:
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__(*groups)

        self.radius: float = 0
        self.velocity: pygame.Vector2 = pygame.Vector2(0, 0)
        self.image: pygame.Surface = pygame.Surface((0, 0))
        self.rect: pygame.Rect = self.image.get_rect()

    def set_attrs(self: "CircleShape", x: float, y: float, radius: float) -> None:
        self.radius = radius
        self.rect.width=int(self.radius*2)
        self.rect.height=int(self.radius*2)
        self.rect.center=(int(x),int(y))

    def draw(self, screen: pygame.Surface) -> None:
        # must override
        pass

    def update(self, dt: float) -> None:
        # must override
        pass

    def collides_with(self, other: "CircleShape") -> bool:
        my_pos=pygame.Vector2(int(self.rect.center[0]),int(self.rect.center[1]))
        other_pos=pygame.Vector2(other.rect.center[0],other.rect.center[1])
        return my_pos.distance_to(other_pos)<=self.radius+other.radius
