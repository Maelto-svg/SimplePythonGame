from element import Element

class Environnement(Element):

    def __init__(self, x, y , push, resist, sprite):
        super().__init__(x, y, sprite)
        self.push = push
        self.resist = resist