import importlib
import json

import pygame
from logger import Logger


class Scene:
    def __init__(self, width, height):
        self.elements = []
        self.grav = 0
        self.player = None
        self.plats = None
        self.env = None  # Added to store environment elements
        self.width = width
        self.height = height
        self.logging = Logger.get_instance()
        self.logging.info(f"Scene created with dimensions {width}x{height}")

    def resize(self, sprite, size):
        """Resize a sprite to specified dimensions."""
        if size == "full":
            dim = [self.width, self.height]
        else:
            try:
                dim = [int(i) for i in size.split("x")]
            except ValueError as e:
                self.logging.error(f"Invalid size format '{size}': {e}")
                raise
        resized_sprite = pygame.transform.scale(sprite, dim)
        self.logging.debug(f"Resized sprite to {dim}")
        return resized_sprite

    # TODO Move it somewhere else
    def load_class(self, class_name, module_name):
        """
        Dynamically loads a class from a given module.
        """
        try:
            module = importlib.import_module(module_name)
            self.logging.debug(f"Successfully imported module '{module_name}'")
            loaded_class = getattr(module, class_name)
            self.logging.debug(
                f"Successfully loaded class '{class_name}' from module '{module_name}'"
            )
            return loaded_class
        except (ImportError, AttributeError) as e:
            self.logging.error(
                f"Error loading class '{class_name}' from module '{module_name}': {e}"
            )
            raise

    def load(self, file, entry):
        """
        Load scene data from a JSON file and initialize elements.
        """
        try:
            with open(file, "r") as f:
                data = json.load(f)
            self.logging.info(f"Loaded scene data from '{file}'")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logging.error(f"Error reading file '{file}': {e}")
            raise

        try:
            content = sorted(data["content"], key=lambda x: x["depth"])
            self.logging.debug("Sorted scene content by depth")
        except KeyError as e:
            self.logging.error(f"Missing 'content' key in scene data: {e}")
            raise

        self.elements = []
        for e in content:
            try:
                # Dynamically import the class and create an instance
                instance_type = e["class"].split(".")
                class_name = instance_type[1]
                module_name = instance_type[0]
                Class = self.load_class(class_name, module_name)

                sprite = pygame.image.load(e["sprite"])
                self.logging.info(
                    f"Loaded sprite '{e['sprite']}' for class '{class_name}'"
                )
                sprite = self.resize(sprite, e["size"])

                if class_name == "Player":
                    e["args"] = data["player_spawn"][entry] + e["args"]
                    self.logging.debug(f"Set player spawn position for entry '{entry}'")

                element_instance = Class(*e["args"], sprite)
                self.elements.append(element_instance)
                self.logging.info(f"Added instance of '{class_name}' to elements")
            except Exception as err:
                self.logging.error(f"Failed to load element {e} because of: {err}")

        try:
            self.player = [
                e for e in self.elements if e.__class__.__name__ == "Player"
            ][0]
            self.logging.debug("Player object initialized")
        except IndexError:
            self.logging.warning(
                "No Player object found in scene elements"
            )  # TODO Create a default instance of player

        self.plats = [e for e in self.elements if e.__class__.__name__ == "Platform"]
        self.logging.info(f"Initialized {len(self.plats)} Platform objects")

        self.env = [e for e in self.elements if e.__class__.__name__ == "Environnement"]
        self.logging.info(f"Initialized {len(self.env)} Environment objects")

        self.grav = data.get("grav", 0)
        self.logging.info(f"Gravity set to {self.grav}")
