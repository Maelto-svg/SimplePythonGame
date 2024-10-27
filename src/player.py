from entity import Entity

class Player(Entity):

    def __init__(self, x,y, speed, acc, sprite):
        super().__init__(x,y, sprite, speed, acc)
        self.cont = 0

    def moveLeft(self):
        self.direction[0] = 1

    def moveRight(self):
        self.direction[1] = 1

    def jump(self):
        if self.cont == 10:
            self.cont = 0
        elif self.onGround or self.cont:
            self.direction[2] = 1-self.cont*0.1
            self.cont += 1
    
    def dive(self):
        self.direction[3] = 1