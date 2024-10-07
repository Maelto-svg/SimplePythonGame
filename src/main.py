import pygame
import numpy as np
from player import Player

def isOnGround(ent):
    ent.onGround = ent.rect.bottom >= height

# pygame setup
pygame.init()
height, width = 720, 1280
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = (screen.get_width() / 2, screen.get_height() / 2)

speed = np.array([0.0,0.0])
acc = np.array([5000,5000,3e4,8000]) #Left, Right, Up, Down
sprite = pygame.image.load("ressources/sprites/resized_player.png")

p1 = Player(player_pos[0],player_pos[1], sprite, speed, acc)

grav = 8000

nat = np.array([0,0,0,0])

ground_resistance = 7
air_resistance = .5

ground_push = [1, 1]
air_push = [0.2, 1]

resistance = [ground_resistance, air_resistance]
push = [ground_push, air_push]

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    screen.blit(p1.sprite, p1.rect)

    p1.direction = np.array([0.0,0.0,0.0,0.0])

    nat = np.array([0,0,0,0])

    if not p1.onGround:
        nat[3] = grav

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        p1.jump()
    else:
        p1.cont = 0
    if keys[pygame.K_LSHIFT]:
       p1.dive()
    if keys[pygame.K_q]:
        p1.moveLeft()
    if keys[pygame.K_d]:
        p1.moveRight()

    p1.varSpeed(nat, resistance, push, dt)

    p1.move(speed[0]*dt, speed[1]*dt)

    isOnGround(p1)

    if p1.onGround:
        p1.rect.bottom = height
        speed[1] = 0
        p1.onGround = True

    # flip() the display to put your work on screen
    pygame.display.flip()
    #print(f"x={p1.x}, y={p1.y}, vit={p1.speed}")
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    #print(f"speed = {speed}, x={player_pos.x}, y={player_pos.y}")

pygame.quit()