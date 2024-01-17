# gom/scene/scene_manager.py
# Handles user controls and interactions in the scene

import math

class SceneManager:
    def __init__(self, scene, renderer, canvas):
        # Initialize the scene manager with the given scene, renderer, and canvas
        self.scene = scene
        self.renderer = renderer
        self.canvas = canvas
        self.renderer.root.bind("<Key>", self.handle_keypress)

    def handle_keypress(self, event):
        # Handle keypress event, exit on "Q" or "q"
        if event.char.lower() == 'q':
            self.renderer.root.destroy()

    def handle_user_input(self):
        # Implement user controls and interactions logic here
        # For simplicity, this example handles only keypress event to exit
        # input("Press q to exit...")

        # Set focus to the canvas
        self.canvas.focus_set()

        # Bind mouse click event to on_mouse_click method
        self.canvas.bind("<Button-1>", self.on_mouse_click)
        self.canvas.bind("<Double-Button-1>", self.on_mouse_double_click)

    def on_mouse_click(self, event):
        # Handle mouse click event here
        print(f"Mouse clicked at {event.x}, {event.y}")

        # Iterate over the elements in the scene's root_assembly
        for element in self.scene.root_assembly.elements:
            # Get coordinates and angle from the pose, assume t(x, y, orientation)
            x, y, orientation = element.pose
            width, height = element.size

            # Calculate the distance between the mouse click and the element
            distance = ((x - event.x)**2 + (y - event.y)**2)**0.5

            # If the distance is less than 10 pixels, the element was selected
            if distance <= 50:
                print(f"Element {element.type} was selected")
                # Update element orientation by 10 degrees
                element.pose = (x, y, orientation + 10)
                # Update the element: polygon on the canvas
                new_points = self.renderer.rotate_points(self.renderer.canvas.coords(element.tkinter_id), math.radians(10), (x, y))
                self.renderer.canvas.coords(element.tkinter_id, *new_points)
            

    def on_mouse_double_click(self, event):
        # Handle mouse double click event here
        print(f"Mouse double clicked at {event.x}, {event.y}")
