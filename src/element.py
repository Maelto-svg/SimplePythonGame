

class Element:

    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite

    def moveTo(self, x, y):
        self.x = x
        self.y = y

    def move(self, vx, vy):
        self.x += vx
        self.y += vy