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
        self.canvas.bind("<Button-1>", self.select_element) # mouse click
        self.canvas.bind("<B1-Motion>", self.move_element) # mouse drag
        self.canvas.bind("<Double-Button-1>", self.rotate_element) # mouse double click


    # TODO update select_element using element points as bounding box
    # TODO refactor: rename and separte the methods and their parts for code reuse & clarity

    def select_element(self, event):
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


    def move_element(self, event):
        '''
        Move Element with mouse drag
        update element pose and polygon coordinates
        '''

        # Iterate over the elements in the scene's root_assembly
        for element in self.scene.root_assembly.elements:
            # Get coordinates and angle from the pose, assume t(x, y, orientation)
            x, y, orientation = element.pose
            width, height = element.size

            # Calculate the distance between the mouse click and the element
            distance = ((x - event.x)**2 + (y - event.y)**2)**0.5

            # If the distance is less than 10 pixels, the element was selected
            # Update element position to new mouse position
            if distance <= 50:
                # Update element in assembly to new mouse position
                element.pose = (event.x, event.y, orientation)
                # Print new element pose
                print(f"Element {element.type} was moved to {element.pose}")
                # Update element on the screen: polygon on the canvas
                points = self.renderer.create_points(event.x, event.y, width, height)
                new_points = self.renderer.rotate_points(points, math.radians(orientation), (event.x, event.y))
                # Fixed bug with points in bad format (float) after movement
                # TODO clean the points reformat code below and in render_elements
                unpacked_points = [point for pair in new_points for point in pair]  # Unpack the points from a list of tuples to a list of numbers
                integer_points = [int(point) for point in unpacked_points]  # Convert the points to integers                
                self.renderer.canvas.coords(element.tkinter_id, integer_points)               
            

    def rotate_element(self, event):
        # Handle mouse double click event here
        print(f"Mouse double clicked at {event.x}, {event.y}")

        # Iterate over the elements in the scene's root_assembly
        for element in self.scene.root_assembly.elements:
            # Get coordinates and angle from the pose, assume t(x, y, orientation)
            x, y, orientation = element.pose
            width, height = element.size

            # Calculate the distance between the mouse click and the element
            distance = ((x - event.x)**2 + (y - event.y)**2)**0.5

            # If the distance is less than 10 pixels, the element was selected
            # Update element orientation by 10 degrees
            if distance <= 50:
                print(f"Element {element.type} was selected")
                # Update element in assembly
                # TODO for testing: orientation by 10 degrees
                # TODO add alignment/aiming to mouse cursor or ray aiming later
                element.pose = (x, y, orientation + 10)
                # Update element on the screen: polygon on the canvas
                points = self.renderer.create_points(x, y, width, height)
                new_points = self.renderer.rotate_points(points, math.radians(orientation + 10), (x, y))
                # Fixed bug with points in bad format (float) after rotation
                # TODO clean the points reformat code below and in render_elements
                unpacked_points = [point for pair in new_points for point in pair]  # Unpack the points from a list of tuples to a list of numbers
                integer_points = [int(point) for point in unpacked_points]  # Convert the points to integers                
                self.renderer.canvas.coords(element.tkinter_id, integer_points)       
