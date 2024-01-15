# gom/scene/scene.py
# Defines the Scene class for managing the entire scene
# Defines the Scene class representing the top-level scene structure using Pygame

from gom.base import Serializable

class Scene(Serializable):
    def __init__(self, root_assembly=[]):
        # Initialize the scene with the root assembly
        self.root_assembly = root_assembly

    def update(self):
        # Update the scene elements, e.g., propagate rays
        pass

    def to_json(self):
        # Convert scene to a JSON-compatible format
        return {
            "root_assembly": self.root_assembly.to_json()
        }

    @staticmethod
    def from_json(data):
        # Create a Scene instance from JSON data
        root_assembly = Serializable.from_json(data["root_assembly"])
        return Scene(root_assembly)
