from element import Element
from pygame.transform import scale

class Platform(Element):

    def __init__(self, x,y, sprite, dim = None): 
        if dim!=None:
            sprite = scale(sprite, dim)
        super().__init__(x, y, sprite)
        
