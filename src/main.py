import pygame
import numpy as np
from scene import Scene

def Collision(ent):
    global push, resistance
    temp_ground = False
    for p in sceen.plats:
        if ent.rect.colliderect(p):
            tab_ent = np.array([
                    ent.rect.right,
                    ent.rect.left,
                    ent.rect.bottom,
                    ent.rect.top
                    ])
            tab_plat = np.array([
                    p.rect.left,
                    p.rect.right,
                    p.rect.top,
                    p.rect.bottom
                    ])
            over = (tab_ent - tab_plat) * np.array([1.0,-1.0,1.0,-1.0])
            if ent.speed[0] >= 0:
                over[1] = np.inf
            else:
                over[0] = np.inf
            if ent.speed[1] >= 0:
                over[3] = np.inf
            else:
                over[2] = np.inf

            bouncing_dir = np.argmin(over)

            ent.speed[bouncing_dir//2] = 0
            if bouncing_dir == 0:
                ent.rect.right = p.rect.left
            elif bouncing_dir == 1:
                ent.rect.left = p.rect.right
            elif bouncing_dir == 2:
                ent.rect.bottom = p.rect.top
                push = [push[i] + p.push[i] for i in range(len(push))]
                resistance += p.resist
            elif bouncing_dir == 3:
                ent.rect.top = p.rect.bottom
            temp_ground = bouncing_dir == 2 or temp_ground

    ent.onGround = temp_ground
    
    if ent.rect.left < 0 or ent.rect.right > width:
        ent.speed[0] = 0
        ent.rect.left = max(0, ent.rect.left)
        ent.rect.right = min(width, ent.rect.right)
    if ent.rect.bottom > height:
        ent.speed[1] = 0
        ent.rect.bottom = height
        ent.onGround = True


def env(ent):
    global push, resistance
    p = ent.rect.collidelist(sceen.env)
    e = sceen.env[p]
    push = [push[i] + e.push[i] for i in range(len(push))]
    resistance += e.resist

# pygame setup
pygame.init()
height, width = 720, 1080
flags = pygame.FULLSCREEN | pygame.SCALED
screen = pygame.display.set_mode((width, height),)
clock = pygame.time.Clock()
running = True
dt = 0

# sceen setup
sceen = Scene(width, height)

sceen.load("ressources/scenes/start.json", 0)

p1 = sceen.player

# physics setup

nat = np.array([0,0,0,0])

resistance = 1
push = [1, 1]


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    for e in sceen.elements:
        screen.blit(e.sprite, e.rect)
        
    p1.direction = np.array([0.0,0.0,0.0,0.0])

    nat = np.array([0,0,0,0])
    nat[3] = sceen.grav

    env(p1)

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

    p1.move(p1.speed[0]*dt, p1.speed[1]*dt)

    resistance = 0
    push = [0, 0]

    Collision(p1)

    # flip() the display to put your work on screen
    pygame.display.flip()
    #print(f"x={p1.x}, y={p1.y}, vit={p1.speed}")
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    #print(f"speed = {speed}, x={player_pos.x}, y={player_pos.y}")

pygame.quit()