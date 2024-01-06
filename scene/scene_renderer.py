# gom/scene/scene_renderer.py
# Handles the graphical rendering of the scene using TkInter canvas

import tkinter as tk
import math
from gom.scene import Scene
from scene.settings import Settings  # Import the Settings class from the scene module

class SceneRenderer:
    def __init__(self, scene, settings=None):
        # Initialize the renderer with the given scene and settings
        self.scene = scene
        self.settings = settings or Settings()
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg=self.settings.background_color)
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
            # Calculate coordinates for rendering a rotated rectangle
            x1 = x - width / 2
            y1 = y - height / 2
            x2 = x + width / 2
            y2 = y + height / 2
            # Convert orientation to radians for rendering
            angle = -orientation  # Negative sign for counterclockwise rotation
            # Calculate rotated coordinates using math functions
            x1r = x + (x1 - x) * math.cos(angle) - (y1 - y) * math.sin(angle)
            y1r = y + (x1 - x) * math.sin(angle) + (y1 - y) * math.cos(angle)
            x2r = x + (x2 - x) * math.cos(angle) - (y2 - y) * math.sin(angle)
            y2r = y + (x2 - x) * math.sin(angle) + (y2 - y) * math.cos(angle)
            # Draw a polygon representing the rotated rectangle with element color
            self.canvas.create_polygon(x1r, y1r, x2r, y1r, x2r, y2r, x1r, y2r, fill=self.settings.element_color, outline='black')

# Example usage:
# settings = Settings()
# scene = Scene(root_assembly=some_assembly_instance)
# renderer = SceneRenderer(scene, settings)
# renderer.render()
