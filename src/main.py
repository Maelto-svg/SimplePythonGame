# Example file showing a circle moving on screen
import pygame
import numpy as np
# pygame setup
pygame.init()
height, width = 720, 1280
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
rad = 40
grav = 8000

speed = np.array([0.0,0.0])
acc = np.array([5000,5000,5e4,8000])
direction = np.array([0.0,0.0,0.0,0.0])
nat = np.array([0,0,0,0])
resistance = 7

mask = np.array([[-1,0],[1,0],[0,-1],[0,1]])
cont = 0

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    pygame.draw.circle(screen, "red", player_pos, rad)

    direction = np.array([0.0,0.0,0.0,0.0])
    nat = np.array([0,0,0,0])

    if player_pos.y < height - rad:
        nat[3] = grav

    keys = pygame.key.get_pressed()
    if cont == 10:
        cont = 0
    elif keys[pygame.K_SPACE] and (player_pos.y == height - rad or cont):
        direction[2] = 1-cont*0.1
        cont += 1
        print(direction[2])
    else:
        cont = 0
    if keys[pygame.K_LSHIFT]:
        direction[3] = 1
    if keys[pygame.K_q]:
        direction[0] = 1
    if keys[pygame.K_d]:
        direction[1] = 1
    
    F = np.dot((direction * acc), mask)
    C = np.dot(nat,mask)
    R = resistance*speed

    speed += (F + C - R)*dt

    if player_pos.y > height - rad:
        player_pos.y = height - rad
        speed[1] = 0

    player_pos.x += speed[0] * dt
    player_pos.y += speed[1] * dt
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    #print(f"speed = {speed}, x={player_pos.x}, y={player_pos.y}")

pygame.quit()