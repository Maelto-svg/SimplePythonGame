from element import Element
import numpy as np

class Entity(Element):
    mask = np.array([[-1,0],[1,0],[0,-1],[0,1]])

    def __init__(self, x,y, sprite, speed, acc):
        super().__init__(x,y,sprite)
        self.speed = speed
        self.acc = acc
        self.direction = np.array([0.0,0.0,0.0,0.0])
        self.onGround = False

    def varSpeed(self, constraint, resistance, time):
        F = np.dot((self.direction * self.acc), self.mask)
        C = np.dot(constraint,self.mask)
        R = resistance*self.speed

        for i in range(2):
            if abs(R[i]*time) > abs(self.speed[i] + (F[i]+C[i])*time):
                self.speed[i] = 0
            else:
                self.speed[i] += (F[i] + C[i] - R[i])*time

    def moveLeft(self):
        pass

    def moveRight(self):
        pass

    def jump(self):
        pass

    