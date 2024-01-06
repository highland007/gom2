# gom/element.py
# Defines the Element class for general optical models

class Element:
    def __init__(self, element_type, size, pose):
        # Initialize an element with type, size, and pose
        self.type = element_type  # 'mirror' or 'lens'
        self.size = size          # Tuple (width, height)
        self.pose = pose          # Tuple (x, y, orientation)
