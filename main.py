import sys

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from gamestate import GameState
from logger import log_event, log_state
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
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    scoreboard=Scoreboard(gamestate)

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                if gamestate.iframes>0:
                    continue
                elif gamestate.lives>1:
                    gamestate.lives-=1
                    player.position=pygame.Vector2(SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
                    gamestate.iframes=60
                else:
                    print("Game over!")
                    sys.exit()
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    shot.kill()
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
