import importlib
import json

import pygame
from logger import Logger


class Scene:
    """
    This class represent the collection of elements that need to be displayed at any given time.
    """

    def __init__(self, width: int, height: int):  # TODO Make it a singleton ?
        """
        Function to initialize a Scene object, it should only be run once.

        :param width: The width in pixel the scene needs to occupy.
        :param height: The height in pixel the scene needs to occupy.
        :returns: a new scene.
        """
        self.elements = []  # List of all element present
        self.grav = 0  # Gravity
        self.player = None  # The player object
        self.plats = None  # All the platforms in the scene
        self.env = None  # All the environnement in the scene
        self.width = width
        self.height = height
        self.logging = Logger.get_instance()
        self.logging.info(f"Scene created with dimensions {width}x{height}")

    def resize(self, sprite: pygame.surface.Surface, size: str):
        """
        Resize a sprite to specified dimensions.

        :param sprite: The sprite to resize.
        :param size: The size to which the sprite needs to be resized.
        Format "widthxheight", or "full" if the element needs to occupy the entire scene.
        :returns: The resized sprite using pygame.transform.scale.
        """
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
    def load_class(self, class_name: str, module_name: str):
        """
        Dynamically loads a class from a given module.

        :param class_name: The name of the class to load.
        :param module_name: The name of the module in which the class is located.
        :returns: Nothing, it simply loads a class
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

    def load(self, file: str, entry: int):
        """
        Load scene data from a JSON file following a specific format and initialize the elements.

        :param file: The JSON file to load.
        :param entry: From which entry points did we access this new scene.
        For instance did we load from the "next" scene or the "previous" one.
        :returns: Nothing it updates all the elements fields in the scene object.
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
        self.logging.info(f"Initialized {len(self.env)} Environnement objects")

        self.grav = data.get("grav", 0)
        self.logging.info(f"Gravity set to {self.grav}")
