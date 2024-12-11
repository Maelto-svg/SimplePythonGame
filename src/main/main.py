import logging

import numpy as np
import pygame
from logger import Logger
from scene import Scene


class Game:
    def __init__(self, width=1080, height=720):
        # Setup logging
        self.logging = Logger.get_instance(level=logging.DEBUG)

        # Pygame setup
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.logging.info("Pygame initialised")

        # Scene setup
        self.scene = Scene(self.width, self.height)
        self.scene.load("ressources/scenes/start.json", 0)
        self.player = self.scene.player

        # Physics setup
        self.nat = np.array([0, 0, 0, 0])
        self.resistance = 1
        self.push = [1, 1]

        self.logging.info("Game ready")

    def collision(self, ent):
        """
        This is a function to detect if there is a collision between an entity and any other.
        It will directly modify the speed and the position of the entity.

        :param ent: the entity to test
        :returns: nothing
        """
        temp_ground = False
        for p in self.scene.plats:
            if ent.rect.colliderect(p):
                self.logging.debug(f"Collision detected: {ent.rect} with {p.rect}")

                tab_ent = np.array(
                    [ent.rect.right, ent.rect.left, ent.rect.bottom, ent.rect.top]
                )
                tab_plat = np.array(
                    [p.rect.left, p.rect.right, p.rect.top, p.rect.bottom]
                )
                over = (tab_ent - tab_plat) * np.array([1.0, -1.0, 1.0, -1.0])

                if ent.speed[0] >= 0:
                    over[1] = np.inf
                else:
                    over[0] = np.inf
                if ent.speed[1] >= 0:
                    over[3] = np.inf
                else:
                    over[2] = np.inf

                bouncing_dir = np.argmin(over)

                ent.speed[bouncing_dir // 2] = 0
                if bouncing_dir == 0:
                    ent.rect.right = p.rect.left
                elif bouncing_dir == 1:
                    ent.rect.left = p.rect.right
                elif bouncing_dir == 2:
                    ent.rect.bottom = p.rect.top
                    self.push = [
                        self.push[i] + p.push[i] for i in range(len(self.push))
                    ]
                    self.resistance += p.resist
                elif bouncing_dir == 3:
                    ent.rect.top = p.rect.bottom
                temp_ground = bouncing_dir == 2 or temp_ground

        ent.onGround = temp_ground

        if ent.rect.left < 0 or ent.rect.right > self.width:
            ent.speed[0] = 0
            ent.rect.left = max(0, ent.rect.left)
            ent.rect.right = min(self.width, ent.rect.right)
            self.logging.debug(
                f"Player collided with horizontal boundary at: {ent.rect}"
            )
        if ent.rect.bottom > self.height:
            ent.speed[1] = 0
            ent.rect.bottom = self.height
            ent.onGround = True
            self.logging.debug(f"Player collided with vertical boundary at: {ent.rect}")

    def env(self, ent):
        """
        This is a function to detect in which environnement an entity is.
        It will directly modify the pushing power and the resistance.

        :param ent: The entity to test
        :returns: Nothing
        """
        p = ent.rect.collidelist(self.scene.env)
        e = self.scene.env[p]
        self.push = [self.push[i] + e.push[i] for i in range(len(self.push))]
        self.resistance += e.resist
        self.logging.debug(
            f"Environmental interaction: Push = {self.push}, Resistance = {self.resistance}"
        )

    def main_loop(self):
        """
        The main game loop.
        """
        while self.running:
            # Poll for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Fill the screen with a color to wipe away anything from last frame
            self.screen.fill("white")
            for e in self.scene.elements:
                self.screen.blit(e.sprite, e.rect)

            self.player.direction = np.array([0.0, 0.0, 0.0, 0.0])

            self.nat = np.array([0, 0, 0, 0])
            self.nat[3] = self.scene.grav

            self.env(self.player)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.player.jump()
            else:
                self.player.cont = 0
            if keys[pygame.K_LSHIFT]:
                self.player.dive()
            if keys[pygame.K_q]:
                self.player.moveLeft()
            if keys[pygame.K_d]:
                self.player.moveRight()

            self.player.varSpeed(self.nat, self.resistance, self.push, self.dt)

            self.player.move(
                self.player.speed[0] * self.dt, self.player.speed[1] * self.dt
            )

            self.resistance = 0
            self.push = [0, 0]

            self.collision(self.player)

            # Flip the display to put your work on screen
            pygame.display.flip()

            # Print the current speed and position (for debugging)
            self.logging.debug(
                f"Player speed: {self.player.speed}, Position: {self.player.rect.topleft}"
            )

            # Limits FPS to 60
            self.dt = self.clock.tick(60) / 1000

        pygame.quit()
        self.logging.critical("Game was terminated by User")


if __name__ == "__main__":
    game = Game()
    game.main_loop()
