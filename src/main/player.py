import numpy as np
import pygame
from entity import Entity


class Player(Entity):
    """
    This class represent the player controlled character.
    """

    def __init__(
        self,
        x: int,
        y: int,
        speed: np.ndarray,
        acc: np.ndarray,
        sprite: pygame.surface.Surface,
    ):
        """
        Function to initialize a Player object.

        :param x: The x coordinate of the player.
        :param y: The y coordinate of the player.
        :param speed: The initial speed of the object, ex [0.0, 0.0]
        :param acc: The maximum accelaration the player can have in every direction, ex [0, 500, 6000, 0]
        :param sprite: This is the sprite that will displayed on the element's position.
        :returns: a new player.
        """
        super().__init__(x, y, sprite, speed, acc)
        # This counts for how many frames has the player been jumping
        self.cont = 0

    def moveLeft(self):
        """
        The function will make it so the player will try to go left on the next frame.
        """
        self.direction[0] = 1

    def moveRight(self):
        """
        The function will make it so the player will try to go right on the next frame.
        """
        self.direction[1] = 1

    def jump(self):
        """
        The function will make it so the player will try to jump on the next frame.
        """
        if self.cont == 10:
            self.cont = 0
        elif self.onGround or self.cont:
            self.direction[2] = 1 - self.cont * 0.1
            self.cont += 1

    def dive(self):
        """
        The function will make it so the player will try to dive to the ground on the next frame.
        """
        self.direction[3] = 1
