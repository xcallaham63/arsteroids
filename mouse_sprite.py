import pygame


class Mouse_sprite(pygame.sprite.Sprite):
    def __init__(self: "Mouse_sprite", *groups) -> None:
        super().__init__(*groups)
        self.rect=pygame.Rect(0,0,1,1)
        self.mask=pygame.mask.Mask((1,1), fill=True)
        self.image=pygame.Surface((1,1))
