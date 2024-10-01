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
grav = 2000

speed = np.array([0.0,0.0])
max_speed = np.array([300,300])
acc = np.array([2100,2100])
dec = np.array([600,600])
fact = acc/max_speed
decFact = dec/max_speed

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    pygame.draw.circle(screen, "red", player_pos, rad)
    
    if player_pos.y < height - rad:
        speed[1] -= grav*dt
    if player_pos.y > height - rad:
        player_pos.y = height - rad
        speed[1] = 0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_z]:
        speed[1] += (-fact[1]*speed[1] + acc[1])*dt
    else:
        speed[1] -= speed[1]*decFact[1]*dt
    if keys[pygame.K_s]:
        speed[1] -= (fact[1]*speed[1] + acc[1])*dt
    else:
        speed[1] -= speed[1]*decFact[1]*dt
    if keys[pygame.K_q]:
        speed[0] += (-fact[0]*speed[0] + acc[0])*dt
    else:
        speed[0] -= speed[0]*decFact[0]*dt
    if keys[pygame.K_d]:
        speed[0] -= (fact[0]*speed[0] + acc[0])*dt
    else:
        speed[0] -= speed[0]*decFact[0]*dt

    player_pos.x -= speed[0] * dt
    player_pos.y -= speed[1] * dt
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    print(f"speed = {speed}, x={player_pos.x}, y={player_pos.y}")

pygame.quit()