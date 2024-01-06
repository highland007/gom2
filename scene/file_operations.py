# gom/scene/file_operations.py
# Handles saving and loading scenes to/from files

import json
from gom.scene import Scene  # Import the Scene class from gom module

class FileOperations:
    def save_scene(self, scene, filename):
        # Serialize the scene object into JSON and save it to a file
        with open(filename, 'w') as file:
            json.dump(scene.to_json(), file, indent=2)

    def load_scene(self, filename):
        # Load a scene from a JSON file and return a Scene object
        with open(filename, 'r') as file:
            data = json.load(file)
            return Scene.from_json(data)
