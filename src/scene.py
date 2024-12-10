import json
import importlib
import pygame


class Scene:

    def __init__(self, width, height):
        self.elements = []
        self.grav = 0
        self.player = None
        self.plats = None
        self.width = width
        self.height = height

    def resize(self, sprite, size):
        if size == "full":
            dim = [self.width, self.height]
        else:
            dim = [int(i) for i in size.split("x")]
        return pygame.transform.scale(sprite, dim)

    # TODO Move the loading mechanism elsewhere
    def load_class(self, class_name, module_name):
        """
        Dynamically loads a class from a given module.
        """
        module = importlib.import_module(module_name)
        return getattr(module, class_name)

    def load(self, file, entry):
        with open(file, 'r') as f:
            data = json.load(f)
        content = sorted(data["content"], key=lambda x: x["depth"])
        self.elements = []
        for e in content:
            # Dynamically import the class and create an instance
            instance_type = e["class"].split(".")
            class_name = instance_type[1]
            module_name = instance_type[0]
            Class = self.load_class(class_name, module_name)

            sprite = pygame.image.load(e["sprite"])
            sprite = self.resize(sprite, e["size"])

            if class_name == "Player":
                e["args"] = data["player_spawn"][entry] + e["args"]

            self.elements.append(Class(*e["args"], sprite))

        self.player = [e for e in self.elements if e.__class__.__name__ == "Player"][0]
        self.plats = [e for e in self.elements if e.__class__.__name__ == "Platform"]
        self.env = [e for e in self.elements if e.__class__.__name__ == "Environnement"]
        self.grav = data["grav"]
