# gom/scene/scene_renderer.py
# Handles the graphical rendering of the scene using TkInter canvas

import tkinter as tk
from gom.scene import Scene  # Import the Scene class from gom module

class SceneRenderer:
    def __init__(self, scene):
        # Initialize the renderer with the given scene
        self.scene = scene
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=800, height=600)
        self.canvas.pack()

    def render(self):
        # Render the scene using the TkInter canvas
        self.render_elements(self.scene.root_assembly.elements)
        self.root.mainloop()

    def render_elements(self, elements):
        # Render all elements on the canvas
        for element in elements:
            # Assume the pose is (x, y, orientation)
            x, y, orientation = element.pose
            width, height = element.size
            # Calculate coordinates and angles for rendering
            x1 = x - width / 2
            y1 = y - height / 2
            x2 = x + width / 2
            y2 = y + height / 2
            # Convert orientation to degrees for rendering
            angle = orientation * 180 / 3.14
            # Draw a rectangle representing the element
            self.canvas.create_rectangle(x1, y1, x2, y2, fill='blue', outline='black', angle=angle)

# Example usage:
# scene = Scene(root_assembly=some_assembly_instance)
# renderer = SceneRenderer(scene)
# renderer.render()
