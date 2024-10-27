import json
from entity import Entity
from Platform import Platform
from element import Element
from player import Player
import pygame

class Scene:

    def __init__(self, width, height):
        self.elements = []
        self.width = width
        self.height = height

    def resize(self, sprite, size):
        if size == "full":
            dim = [self.width, self.height]
        else:
            dim = [int(i) for i in size.split("x")]
        return pygame.transform.scale(sprite, dim)

    def load(self, file, entry):
        with open(file,'r') as f:
            data = json.load(f)
        content = sorted(data["content"], key=lambda x: x["depth"])
        self.elements = []
        for e in content:
            sprite = pygame.image.load(e["sprite"])
            sprite = self.resize(sprite, e["size"])
            if e["class"] == "Player":
                e["args"] = data["player_spawn"][entry] + e["args"] 
            print(e["args"], e["class"])
            self.elements.append(globals()[e["class"]](*e["args"], sprite))
        
        
