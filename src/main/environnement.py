import numpy as np
import pygame
from element import Element


class Environnement(Element):
    """
    This class represent whether there is air water or any other fluid in a certain zone.
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
        Function to initialize an Environnement object.

        :param x: The x coordinate of the element.
        :param y: The y coordinate of the element.
        :param push: How well can an entity in this element exercise it's pushing power, that is move.
        :param resist: How hard it is to move in this environnement, represent "air" resistance.
        :param sprite: This is the sprite that will displayed on the element's position.
        :returns: a new environnement.
        """
        super().__init__(x, y, sprite)
        self.push = push
        self.resist = resist
