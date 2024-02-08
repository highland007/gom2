# gom/scene/scene.py
# Defines the Scene class for managing the entire scene

from gom.base import Serializable

class Scene(Serializable):
    def __init__(self, root_assembly, ray):
        # Initialize the scene with the root assembly
        self.root_assembly = root_assembly
        self.ray = ray

        # TODO Print the scene initialization for debugging ray trace updates
        print(f"Scene init: root_assembly id={id(root_assembly)}, ray id={id(ray)}")

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
