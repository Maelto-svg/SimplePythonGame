import pygame


class Element:
    """
    This is the base class for all element on screen in the game.
    """

    def __init__(self, x: int, y: int, sprite: pygame.surface.Surface):
        """
        Function to initialize an Element object.

        :param x: the x coordinate of the element.
        :param y: the y coordinate of the element.
        :param sprite: this is the sprite that will displayed on the element's position.
        :returns: a new element.
        """
        self.sprite = sprite
        self.rect = self.sprite.get_rect()
        self.move(x, y)

    def move(self, vx: float, vy: float):
        """
        This is a function to move an element of vx horizontally and vy vertically.

        :param vx: The amount to move horizontally.
        :param vy: The amount to move vertically.
        :returns: Nothing the function modify the position directly
        """
        self.rect = self.rect.move(vx, vy)

    def flip(self, Hor: bool, Vert: bool):
        """
        This function flips the element sprite.

        :param Hor: whether or not flipping the sprite horizontally.
        :param Vert: whether or not flipping the sprite vertically.
        :returns: Nothing the function rotate the sprite directly.
        """
        self.sprite = pygame.transform.flip(self.sprite, Hor, Vert)
