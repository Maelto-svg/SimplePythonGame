import numpy as np
from element import Element
from logger import Logger


class Entity(Element):
    mask = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]], dtype=float)

    def __init__(self, x, y, sprite, speed, acc):
        super().__init__(x, y, sprite)
        self.speed = np.array(speed)
        self.acc = np.array(acc)
        self.direction = np.array([0.0, 0.0, 0.0, 0.0])
        self.onGround = False
        self.orient = 1
        self.logging = Logger.get_instance()

    def varSpeed(self, constraint, resistance, push, time):
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

    def moveLeft(self):
        pass

    def moveRight(self):
        pass

    def jump(self):
        pass
