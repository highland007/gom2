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
        self.tkinter_segment_id = None    # TODO Store the TkInter ID of the element segment for rendering

        # Segment the element (pose, width from size) into parametric form (x,y,dx,dy) for ray tracing & rendering
        self.update_segment()
        

    def update_segment(self):
        '''
        Update the element segment with new element pose and size
        '''
        self.element_segment = create_element_segment(self)


    def trace_ray(self, ray):
        '''
        Trace a ray through the element
        Input: incident ray pose (x, y, angle)
        Output: reflected ray pose (x, y, angle)
        '''
        # Trace the ray through the element and return the reflected ray
        return calculate_reflection(ray, self.element_segment)


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
