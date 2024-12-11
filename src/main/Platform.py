import numpy as np
import pygame
from element import Element


class Platform(Element):
    """
    This class represent anything an entity can step on and cannot traverse.
    """

    def __init__(
        self,
        x: int,
        y: int,
        push: np.ndarray,
        resist: float,
        sprite: pygame.surface.Surface,
    ):
        """
        Function to initialize a Platform object.

        :param x: The x coordinate of the platform.
        :param y: The y coordinate of the platform.
        :param push: How well can an entity exercise it's pushing power on this platform, that is move.
        :param resist: How hard it is to move on this platform, represent friction.
        :param sprite: This is the sprite that will displayed on the platform's position.
        :returns: a new platform.
        """
        super().__init__(x, y, sprite)
        self.push = push
        self.resist = resist
