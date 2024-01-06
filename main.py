# main.py
# Entry point to run the application

from gom.scene import Scene
from scene.scene_renderer import SceneRenderer
from scene.scene_manager import SceneManager

def main():
    # Create an example scene (replace with your actual scene setup)
    scene = Scene(root_assembly=None)  # Replace 'None' with your root assembly instance

    # Create a scene renderer and manager
    renderer = SceneRenderer(scene)
    manager = SceneManager(scene, renderer)

    # Run the renderer and manager
    renderer.render()
    manager.handle_user_input()

if __name__ == "__main__":
    main()
