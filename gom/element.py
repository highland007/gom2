# gom/element.py
# Defines the Element class for general optical models

from gom.base import Serializable

class Element(Serializable):
    def __init__(self, element_type, size, pose):
        # Initialize an element with type, size, and pose
        self.type = element_type  # 'mirror' or 'lens'
        self.size = size          # Tuple (width, height)
        self.pose = pose          # Tuple (x, y, orientation)

    def to_json(self):
        # Convert element to a JSON-compatible format
        return {
            "type": self.type,
            "size": self.size,
            "pose": self.pose
        }

    @staticmethod
    def from_json(data):
        # Create an Element instance from JSON data
        return Element(data["type"], data["size"], data["pose"])
