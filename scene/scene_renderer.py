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
        # Set the focus to the canvas widget after rendering
        self.canvas.focus_set()


    def render_elements(self, elements):
        # Render all elements on the canvas
        # TODO fixing bug with points in bad format after rotation
        # TODO additional lines for testing purposes, remove later
        for element in elements:
            # Get coordinates and angle from the pose, assume t(x, y, orientation)
            x, y, orientation = element.pose
            width, height = element.size
            # Calculate coordinates for the rectangle's corners with rotation
            points = self.create_rotated_points(x, y, orientation, width, height)
            # Create polygon representing the rectangle with rotation
            poly = self.canvas.create_polygon(points, outline=self.settings.element_outline, fill=self.settings.element_fill)  # Assign the polygon's ID to poly
            # Store the ID of the polygon in the element's tkinter_id attribute
            element.tkinter_id = poly


    # TODO update create_points method to create_rotated_points method
    # TODO store points in element object? Used for collision / selection detection, rescaling, etc.
    # TODO move these methods to a separate class for polygon manipulation, in Element class?

    # TODO old create_points method, remove later
    def create_points(self, x, y, width, height):
        # Calculate coordinates for the rectangle's corners without rotation
        # Use "bellybutton" coordinates (center of the front face) as the origin
        x1 = x - width / 2
        x2 = x + width / 2
        y1 = y
        y2 = y + height
        # Create polygon representing the rectangle without rotation
        return (x1, y1, x2, y1, x2, y2, x1, y2)
    
    # TODO new create_rotated_points method, keep
    def create_rotated_points(self, x, y, angle, width, height):
        """
        Create a set of points for rotated rectangle.
        Input: x, y, angle, width, height
        Return: points Integer tuple
        """
        # Calculate coordinates for the rectangle's corners without rotation
        # Use "bellybutton" coordinates (center of the front face) as the origin
        x1 = x - width / 2
        x2 = x + width / 2
        y1 = y
        y2 = y + height
        # Create points representing the rectangle without rotation
        points = (x1, y1, x2, y1, x2, y2, x1, y2)
        # Rotate the points around the "bellybutton" and return the rotated points
        rotated_points = self.rotate_points(points, math.radians(angle), (x,y))
        # Convert the rotated points to integers to avoid TkInter bug with float coordinates
        integer_points = [int(point) for point in rotated_points]
        return integer_points

    def rotate_points(self, points, angle, center):
        """
        Rotate a point clockwise by a given angle around a given origin.
        Input: points Tuple, angle Float, center Tuple
        Return: rotated_points flattened list of points
        """
        rotated_points = [(math.cos(angle) * (px-center[0]) + math.sin(angle) * (py-center[1]) + center[0],
                          -math.sin(angle) * (px-center[0]) + math.cos(angle) * (py-center[1]) + center[1]) for px, py in zip(points[::2], points[1::2])]
        return [point for pair in rotated_points for point in pair]  # Flatten the list of tuples to a flat list of points

