# main.py
# Entry point to run the application

from gom.assembly import Assembly
from gom.element import Element
from gom.scene import Scene
from scene.scene_renderer import SceneRenderer
from scene.scene_manager import SceneManager

def main():
    # Create a simple test assembly with two elements (replace with your assembly setup)
    # pose is (x, y, orientation) in pixels and angle in degrees
    test_assembly = Assembly(pose=(0, 0, 0))
    test_assembly.add_element(Element(element_type="mirror", size=(100, 25), pose=(200, 100, 0)))
    test_assembly.add_element(Element(element_type="mirror", size=(125, 35), pose=(400, 400, 60)))


    # Create the scene with the test assembly as the root assembly
    scene = Scene(root_assembly=test_assembly)

    # Create a scene renderer and manager
    renderer = SceneRenderer(scene)
    manager = SceneManager(scene, renderer)

    # Run the renderer and manager
    renderer.render()
    manager.handle_user_input()

if __name__ == "__main__":
    main()
