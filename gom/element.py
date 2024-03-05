# gom/element.py
# Defines the generic Element class for general optical models

from gom.base import Serializable
from gom.parametric import create_element_segment

class Element(Serializable):
    def __init__(self, pose, size, element_type):
        self.pose = pose
        self.size = size
        self.type = element_type
        self.tkinter_id = None
        self.tkinter_segment_id = None
        self.update_segment()

    def update_segment(self):
        self.element_segment = create_element_segment(self)

    def trace_ray(self, ray, power):
        raise NotImplementedError("trace_ray method must be implemented in the derived class")

    def to_json(self):
        return {
            "type": self.type,
            "size": self.size,
            "pose": self.pose
        }

    @staticmethod
    def from_json(data):
        element_type = data["type"]
        if element_type == "mirror":
            return Mirror(data["pose"], data["size"])
        elif element_type == "lens":
            return Lens(data["pose"], data["size"])
        elif element_type == "xtal":
            return Xtal(data["pose"], data["size"])
        else:
            raise ValueError(f"Unknown element type: {element_type}")
