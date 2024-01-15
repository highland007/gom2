# gom/scene/scene_renderer.py
# Handles the graphical rendering of the scene using TkInter canvas

from tkinter import *
import math
from gom.scene import Scene
from scene.settings import Settings  # Import the Settings class from the scene module

class SceneRenderer:
    def __init__(self, scene, settings=None):
        # Set the scene and display settings
        self.scene = scene
        self.settings = settings or Settings()
        # Initialize the renderer with a TkInter canvas and reconfigure for single infinite grid
        self.root = Tk()
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.canvas = Canvas(self.root, width=self.settings.window_width, height=self.settings.window_height, bg=self.settings.background_color, highlightthickness=0)
        self.canvas.grid(column=0, row=0, sticky=(N, W, E, S))

    def render(self):
        # Render the scene using the TkInter canvas
        self.render_elements(self.scene.root_assembly.elements)
        # Set the focus to the canvas widget
        self.canvas.focus_set()
        # Run the TkInter main loop
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
            
