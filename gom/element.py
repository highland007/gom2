# gom/element.py
# Defines the Element class for general optical models

from gom.base import Serializable
from gom.parametric import create_element_segment, create_ray_segment, find_intersection, calculate_reflection

class Element(Serializable):
    def __init__(self, pose, size, element_type):
        # Initialize an element with type, size, and pose
        self.pose = pose          # Tuple (x, y, orientation) not real pose - TODO (matrix 3x3 for 2D)        
        self.size = size          # Tuple (width, height)
        self.type = element_type  # 'mirror' or 'lens'
        self.tkinter_id = None    # Store the TkInter ID of the element for rendering
        self.tkinter_line_id = None    # TODO Store the TkInter ID of the element segment for rendering
        # Segment the element (pose, width from size) into parametric form (x,y,dx,dy) for ray tracing
        self.element_segment = create_element_segment(self.pose, self.size[0])

    def trace_ray(self, ray):
        '''
        Trace a ray through the element
        Input: incident ray pose (x, y, angle)
        Output: reflected ray pose (x, y, angle)
        '''
        # For now, just reflect the ray with a mirror adding 10 degrees to the angle
        # TODO add real mirror physics, angle and position calculations

        reflected_angle = calculate_reflection(ray, self.element_segment)

        # Shift the ray a small amount to avoid self-intersection
        ds = 1e-0
        # return (ray[0] - ds, ray[1] - ds, ray[2] + 135)

        # Flip the ray angle due to screen coordinates
        # TODO check angle flip / convention for the ray
        return (ray[0], ray[1], -reflected_angle)


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
