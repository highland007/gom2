# main.py
# Entry point to run the application

import logging
from gom.assembly import Assembly
from gom.mirror import Mirror
from gom.xtal import Xtal
from gom.ray import Ray
from gom.scene import Scene
from scene.scene_renderer import SceneRenderer
from scene.scene_manager import SceneManager


def main():
    # Set the logging level to DEBUG for detailed output to the log file
    logging.basicConfig(filename='gom2.log', filemode='w', level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')

    # Create a simple test assembly with two elements (replace with your assembly setup)
    # pose is (x, y, orientation) in pixels and angle in degrees
    test_assembly = Assembly(pose=(0, 0, 0))
    test_assembly.add_element(Mirror(pose=(400, 100, 135), size=(200, 25)))
    test_assembly.add_element(Mirror(pose=(400, 400, -45), size=(200, 35), reflectivity=0.9))
    test_assembly.add_element(Xtal(pose=(600, 400, 0), size=(30, 100), gain=2.0, acceptance=(30, 10)))
    test_assembly.add_element(Mirror(pose=(800, 400, 45), size=(100, 45)))

    # Create a test ray with an initial pose (x, y, angle)
    test_ray = Ray(pose=(100, 100, 0))

    # Trace the ray through the test assembly and print the ray path possibly to the console/file
    # test_ray.trace_ray(test_assembly)
    # print(test_ray.ray_path)


    # Create the scene with the test assembly as the root assembly and ray
    scene = Scene(root_assembly=test_assembly, ray=test_ray)
   
    # Create a scene renderer and manager, and pass the scene and renderer to the manager
    # Ray tracing and rendering is done by the renderer, user input by the manager
    renderer = SceneRenderer(scene)
    manager = SceneManager(scene, renderer, renderer.canvas)

    # Run the renderer to render the scene and manager to capture user input
    renderer.render()
    manager.handle_user_input()

    # Start the Tkinter event loop with the renderer's root window, accesible to the manager
    renderer.root.mainloop()


if __name__ == "__main__":
    main()
