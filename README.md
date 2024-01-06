# Game of Mirrors 2D (gom2)

## Overview
Game of Mirrors 2D (gom2) is a Python-based puzzle game where players manipulate elements like mirrors and lenses to direct a laser beam towards a target.

## Structure
- **Assembly**: Groups game elements, handling their collective behavior.
- **Scene**: Manages the overall game environment.
- **SceneManager**: Responsible for saving/loading game scenes to/from JSON files.
- **SceneRenderer**: Handles all graphical rendering using a library (e.g., TkInter).

## Development Approach
- **Modularity**: Code is divided into separate modules for ease of maintenance and scalability.
- **Single Responsibility Principle**: Each module/class has a clear, distinct purpose.
- **Flexibility**: Renderer and file manager are independent, allowing for easy library swaps or logic changes.

## Running the Game
- Run `main.py` to start the game.
- Ensure all dependencies are installed.

## Future Development
- Implement game logic in `assembly.py`.
- Complete save/load functionality in `scene_manager.py`.
- Develop the rendering system in `scene_renderer.py`.
- Flesh out the game loop in `main.py`.
