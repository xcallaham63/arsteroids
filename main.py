import sys

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import PLAYER_RADIUS, SCREEN_HEIGHT, SCREEN_WIDTH
from gamestate import GameState
from logger import log_event, log_state
from mouse_sprite import Mouse_sprite
from player import Player
from scoreboard import Scoreboard
from shot import Shot


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock=pygame.time.Clock()
    dt=0.0
    gamestate=GameState()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Player.containers = (updatable, drawable)
    Shot.containers = (updatable, drawable, shots)
    Scoreboard.containers = (updatable, drawable)

    asteroidfield = AsteroidField()
    player = Player()
    player.set_attrs(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, PLAYER_RADIUS)
    scoreboard=Scoreboard(gamestate)
    log_event("game_start")

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        updatable.update(dt)

        # testing player hitbox
        screen.blit(player.mask_surface, player.rect)

        # debugging to figure out why my player-asteroid collisions aren't being detected
        mouse_sprite=Mouse_sprite()
        mouse_sprite.rect.topleft=pygame.mouse.get_pos()
        if player.rect.collidepoint(mouse_sprite.rect.topleft):
            print("mouse collision with player rect detected")
            if pygame.sprite.collide_mask(player,mouse_sprite):
                print("actual collision with player detected")
                rel_x = mouse_sprite.rect.x - player.rect.x
                rel_y = mouse_sprite.rect.y - player.rect.y
                if bool(player.mask.get_at((rel_x, rel_y))):
                    print("the bool worked too")

        ast_player_hits: list[pygame.sprite.Sprite] = pygame.sprite.spritecollide(player, asteroids, False, pygame.sprite.collide_mask)
        for asteroid in ast_player_hits:
            print("there was a hit!")
            if gamestate.iframes>0:
                continue
            else:
                log_event("player_hit")
                if gamestate.lives>1:
                    gamestate.lives-=1
                    player.rect.center=(int(SCREEN_WIDTH/2),int(SCREEN_HEIGHT/2))
                    gamestate.iframes=60
                else:
                    print("Game over!")
                    sys.exit()

        ast_shot_hits: dict[Shot, list[Asteroid]] = pygame.sprite.groupcollide(shots, asteroids, False, False, pygame.sprite.collide_circle)
        for shot, asts in ast_shot_hits.items():
            log_event("asteroid_shot")
            shot.kill()
            for asteroid in asts:
                asteroid.split()
            gamestate.score+=1

        for thing in drawable:
            thing.draw(screen)
        pygame.display.flip()
        dt=clock.tick(60)/1000
        if gamestate.iframes>0:
            gamestate.iframes-=1

if __name__ == "__main__":
    main()
