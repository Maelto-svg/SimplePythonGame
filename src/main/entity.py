import numpy as np
import pygame
from element import Element
from logger import Logger


class Entity(Element):
    """
    This class is the general class representing all elements that have an ai, or are player controlled.
    """

    # A mathematical object we use when updating the speed
    mask = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]], dtype=float)

    def __init__(
        self,
        x: int,
        y: int,
        sprite: pygame.surface.Surface,
        speed: np.ndarray,
        acc: np.ndarray,
    ):
        """
        Function to initialize an Entity object.

        :param x: The x coordinate of the element.
        :param y: The y coordinate of the element.
        :param sprite: This is the sprite that will displayed on the element's position.
        :param speed: The initial speed of the object, ex [0.0, 0.0]
        :param acc: The maximum acceleration the entity can have in every direction, ex [0, 500, 6000, 0]
        :returns: a new entity.
        """
        super().__init__(x, y, sprite)
        self.speed = np.array(speed)
        self.acc = np.array(acc)
        self.direction = np.array([0.0, 0.0, 0.0, 0.0])
        self.onGround = False
        self.orient = 1  # Looking right or left
        self.logging = Logger.get_instance()

    def varSpeed(
        self, constraint: np.ndarray, resistance: float, push: np.ndarray, time
    ):
        """
        This function calculates the new speed of the entity after time has passed and updates it.

        :param constraint: This represent the forces applied to the entity outside of its control, like gravity.
        :param resistance: This represent global resistance (air + ground resistance).
        :param push: This represent how well the entity can push or it's adherence. For instance, it is harder to move on ice.
        :param time: How much time has passed since the speed has last been updated.
        :returns: Nothing the function directly updates the speed.
        """
        self.logging.debug(
            f"varSpeed called with constraint={constraint}, resistance={resistance}, "
            f"push={push}, time={time}"
        )
        try:
            F = np.dot((self.direction * self.acc), self.mask) * push
            C = np.dot(constraint, self.mask)
            R = resistance * self.speed

            for i in range(2):
                if abs(R[i] * time) > abs(self.speed[i] + (F[i] + C[i]) * time):
                    self.speed[i] = 0
                else:
                    self.speed[i] += (F[i] + C[i] - R[i]) * time

            if self.orient * self.speed[0] < 0:
                self.flip(True, False)
                self.orient *= -1
                self.logging.info("Entity flipped due to orientation change")
        except Exception as e:
            self.logging.error(f"Error in varSpeed: {e}", "reseting speed to 0")
            self.speed[0] = 0
            self.speed[1] = 0

    # It is assumed that all entities can do that much,
    # but the actual implementation is left to the child classes,
    # as they may vary massively.
    def moveLeft(self):
        pass

    def moveRight(self):
        pass

    def jump(self):
        pass
