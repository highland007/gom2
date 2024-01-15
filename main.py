# main.py
# Main script to run the Game of Mirrors 2D using Pygame

from gom.assembly import Assembly
from gom.element import Element
from gom.scene import Scene
from scene.scene_renderer import SceneRenderer
from scene.scene_manager import SceneManager


def main():
    # Create a simple root assembly with one element (replace with your assembly setup)
    root_assembly = Assembly(pose=(0, 0, 0))
    root_assembly.add_element(Element(element_type="mirror", size=(100, 25), pose=(200, 100, 0.5)))
    root_assembly.add_element(Element(element_type="mirror", size=(100, 25), pose=(400, 200, 1)))    

    # Create the scene with the root assembly
    scene = Scene(root_assembly=root_assembly)

    # Create the scene renderer and manager
    renderer = SceneRenderer(scene)
    manager = SceneManager(renderer)
    
    # Run the scene
    while not manager.quit_requested:
        manager.run()
        renderer.quit()

if __name__ == "__main__":
    main()
