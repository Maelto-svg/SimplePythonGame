import pygame

class Element:

    def __init__(self, x, y, sprite):
        self.sprite = sprite
        self.rect = self.sprite.get_rect()

    def move(self, vx, vy):
        self.rect = self.rect.move(vx, vy)
    
    def flip(self, Hor, Vert):
        self.sprite = pygame.transform.flip(self.sprite, Hor, Vert)