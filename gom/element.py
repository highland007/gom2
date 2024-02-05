# gom/element.py
# Defines the Element class for general optical models

from gom.base import Serializable

class Element(Serializable):
    def __init__(self, pose, size, element_type):
        # Initialize an element with type, size, and pose
        self.pose = pose          # Tuple (x, y, orientation)        
        self.size = size          # Tuple (width, height)
        self.type = element_type  # 'mirror' or 'lens'
        self.tkinter_id = None    # Add this line to store the TkInter ID of the element for rendering

    def trace_ray(self, ray_pose):
        '''
        Trace a ray through the element
        Input: ray_pose (x, y, angle)
        Output: reflected_ray_pose (x, y, angle)
        '''
        # For now, just reflect the ray with a mirror adding 10 degrees to the angle
        # TODO add real mirror physics, angle and position calculations
        return (ray_pose[0], ray_pose[1], ray_pose[2] + 225)
        # return (ray_pose[0], ray_pose[1], ray_pose[2] + 10)

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
