# 2D Game Development Tutorial

## Introduction

Welcome to the 2D Game Development Tutorial! This guide will walk you through the basics of our game project, helping you understand the core concepts, setup, and initial development process.

## Prerequisites

Before starting, ensure you have:
- Python 3.8 or higher installed
- Basic understanding of Python programming
- Git installed (for version control)
- A code editor (VS Code, PyCharm, etc.)

## Setting Up the Development Environment

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/2d-game-project.git
cd 2d-game-project
```

### 2. Create a Virtual Environment

Virtual environments help manage project dependencies:

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Project Structure Overview

Understanding the project structure is crucial:

```
2d-game-project/
│
├── src/                # Main source code
│   ├── main.py         # Entry point of the game
│   ├── player.py       # player class
│   ├──...
├── utils/              # Utility functions
│
├── tests/              # Unit and integration tests
├── docs/               # Documentation
└── requirements.txt    # Project dependencies
```

## Basic Game Mechanics Tutorial

### Creating a Basic Game Object

Let's create a simple player character:

```python
import pygame
from player import Player

img = "/ressources/sprites/placeHolder.png"
sprite = pygame.image.load(img)

player_1 = Player(
    0,              # The x coordinate
    0,              # The y coordinate
    [0.0, 0.0],     # The initial speed
    [1, 1, 1, 1],   # The potential acceleration in every direction
    sprite          # The sprite of our character
)

```

But right now our character is not part of a game, and no game was created.

### Initializing the Game Window
If we run:
```python
from main import Game

game = Game()
game.run()
```
We will open a new game. But our little character is not there, so how do we add him?

### Creating a Scene
To display a certain set of object we create a scene.

To do so we first need to create a JSON file that will contain all the information we need
```JSON
{
    "content": [
        {
            "class": "player.Player",
            "sprite": "ressources/sprites/resized_player.png",
            "size": "64x64",
            "args": [
                [
                    0.0,
                    0.0
                ],
                [
                    1,
                    1,
                    1,
                    1
                ]
            ],
            "depth": 2
        }
    ],
    "player_spawn": [
        [
            0,
            0
        ]
    ],
    "exits": [],
    "grav": 20
}
```
The content array will contain everything we want to display. Each entry is a JSON object with four attributes:
 - class : the class of the object, in this case player but there are others.
 - sprite : the sprite of the object.
 - size : how big should the object be when displayed.
 - args : the other arguments that are necessary to create the object, in this the speed and the acceleration.

The position of a player object is determined by the player_spawn field.

Now to load this we need to run something like this:
```python
from scene import Scene

WIDHT = 1000
HEIGHT = 1000

json = "ressources/scenes/ourJSON.json"

our_scene = Scene(WIDTH, HEIGHT)
our_scene.load(json)

```
### Putting It All Together
A game object already has a scene property so all we need to do is:

```python
from main import Game

def main():
    json = "ressources/scenes/ourJSON.json"
    game = Game()
    game.scene.load(json)
    game.run()

if __name__ == '__main__':
    main()
```

## Common Development Tasks

### Running the Game

```bash
python main.py
```

### Running Tests

```bash
python -m pytest tests/
```

### Code Quality Check

```bash
flake8
```

## Troubleshooting

### Common Issues
- Ensure all dependencies are installed
- Check Python version compatibility
- Verify virtual environment activation

### Pygame Installation Problems
If you encounter issues with Pygame:
```bash
pip install --upgrade pip
pip install pygame
```

## Next Steps

- Implement player movement controls
- Add game assets (sprites, backgrounds)
- Create game levels
- Implement game mechanics

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Resources

- [Pygame Documentation](https://www.pygame.org/docs/)
- [Python Game Development Tutorials](https://realpython.com/pygame-a-primer/)

## License

This project is open-source. Please check the LICENSE file for details.

---

**Happy Game Development!** 🎮🐍
