from element import Element
from pygame.transform import scale

class Platform(Element):

    def __init__(self, x,y,  push, resist, sprite): 
        super().__init__(x, y, sprite)
        self.push = push
        self.resist = resist
