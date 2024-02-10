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
        self.ray_id = None
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
        self.render_ray(self.scene.ray)
        # Set the focus to the canvas widget after rendering
        self.canvas.focus_set()


    def render_elements(self, elements):
        # Render all elements on the canvas
        for element in elements:
            # Calculate coordinates for the rectangle's corners with rotation
            polygon_points = self.create_rotated_points(element)
            # Create polygon representing the rectangle with rotation
            poly = self.canvas.create_polygon(polygon_points, outline=self.settings.element_outline, fill=self.settings.element_fill)  # Assign the polygon's ID to poly
            # Store the ID of the polygon in the element's tkinter_id attribute
            element.tkinter_id = poly


    def update_element(self, element):
        # Calculate coordinates for the rectangle's corners with rotation
        updated_points = self.create_rotated_points(element)
        # Create polygon representing the rectangle with rotation
        self.canvas.coords(element.tkinter_id, updated_points)


    def render_ray(self, ray):
        # Trace ray through the elements and render the ray path
        ray.trace_ray(self.scene.root_assembly)
        # Get the ray points from the ray path as a list of tuples (x, y)
        ray_points = []
        for ray_segment in ray.ray_path:
            ray_points.append(ray_segment[0:2])
        print(f"Ray points: {ray_points}")
        # Draw a ray as segmented line, disabled state to avoid user interaction
        if self.ray_id is None:
            self.ray_id = self.canvas.create_line(ray_points, fill=self.settings.ray_color, state='disabled')
        else:
            #  Asterisk (*) because coords expects separate arguments for each coordinate, not a list of coordinates
            self.canvas.coords(self.ray_id, *ray_points)

        # TODO print assembly and ray ids for debugging
        print(f"SceneRenderer update_ray: root_assembly id={id(self.scene.root_assembly)}, ray id={id(self.scene.ray)}")
        print(f"SceneRenderer update_ray: root_assembly id={id(self.scene.root_assembly)}, ray id={id(ray)}")



    def create_rotated_points(self, element):
        """
        Create a set of points for rotated rectangle.
        Input: x, y, angle, width, height
        Return: points Integer tuple
        """
        # Get coordinates and angle from the pose, assume (x, y, orientation)
        x, y, orientation = element.pose
        width, height = element.size
        # Calculate coordinates for the rectangle's corners without rotation
        # Use "bellybutton" coordinates (center of the front face) as the origin
        x1 = x - width / 2
        x2 = x + width / 2
        y1 = y
        y2 = y + height
        # Create points representing the rectangle without rotation
        points = [x1, y1, x2, y1, x2, y2, x1, y2]
        # Rotate the points around the "bellybutton" and return the rotated points
        rotated_points = self.rotate_points(points, math.radians(orientation), (x,y))
        # Convert the rotated points to integers to avoid TkInter bug with float coordinates
        integer_points = [int(point) for point in rotated_points]
        return integer_points


    def rotate_points(self, points, angle, center):
        """
        Rotate a point clockwise by a given angle around a given origin.
        Input: points List, angle Float, center Tuple
        """
        for i in range(0, len(points), 2):
            px, py = points[i], points[i+1]
            points[i] = math.cos(angle) * (px - center[0]) + math.sin(angle) * (py - center[1]) + center[0]
            points[i+1] = -math.sin(angle) * (px - center[0]) + math.cos(angle) * (py - center[1]) + center[1]
        return points
