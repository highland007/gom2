# main.py
# Main script to run the Game of Mirrors 2D using Pygame

from gom.scene import Scene
from scene.scene_renderer import SceneRenderer
from scene.scene_manager import SceneManager

def main():
    scene = Scene()  # You should pass the appropriate parameters based on your scene structure
    renderer = SceneRenderer(scene)
    manager = SceneManager(renderer)
    
    while not manager.quit_requested:
        manager.run()
        renderer.quit()

if __name__ == "__main__":
    main()
