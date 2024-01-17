# gom/scene/scene_manager.py
# Handles user controls and interactions in the scene

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

    def on_mouse_click(self, event):
        # Handle mouse click event here
        print(f"Mouse clicked at {event.x}, {event.y}")

