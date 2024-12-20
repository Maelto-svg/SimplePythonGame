# 2D Game Project

## Project Description
This is an ongoing 2D game development project in Python. The game is currently under active development, with new features and improvements being added regularly.

## Prerequisites
- Python 3.8+ recommended
- pip (Python package installer)
- Sphinx (for documentation generation)
- Make

## Setup and Installation

### 1. Create a Virtual Environment (Recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the Game
```bash
python main.py
```

## Documentation Generation

### Prerequisites for Documentation
Ensure you have Sphinx and Make installed:
```bash
pip install sphinx
```

### Generating Documentation
Navigate to the `/docs` folder and run:
```bash
cd docs
make html
```

The generated documentation will be available in the `docs/_build/html` directory. Open `index.html` in your web browser to view the documentation.

## Development

### Code Quality

#### Static analysis
You can run static code analysis using:
```bash
flake8
```
flake8 is installed when running ```pip install -r requirements.txt```.

If flake8 was not installed run ```pip install flake8```

#### Pre commit hooks

Static code analysis can be run on commit via pre commit hooks.

To activate them run
```bash
pre-commit install
```

pre-commit is installed when running ```pip install -r requirements.txt```.

If pre-commit was not installed run ```pip install pre-commit```

## Requirements
The `requirements.txt` file includes all necessary dependencies for the project, including:
- Game development libraries
- Code analysis tools
- Documentation generation tools
- Testing frameworks

### Key Dependencies
- `flake8`: Static code analysis tool
- `sphinx`: Documentation generation tool
- Other game-specific libraries (to be specified based on project needs)

## Contributing
1. Fork the repository
2. Create a virtual environment
3. Install dependencies
4. Run `flake8` to ensure code quality
5. Update documentation as needed
6. Submit a pull request

## Current Status
:construction: **Project Under Active Development** :construction:
