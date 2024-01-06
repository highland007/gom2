# gom/assembly.py
# Defines the Assembly class for general optical models

class Assembly:
    def __init__(self, pose):
        self._elements = []  # Private list to store elements or sub-assemblies
        self._pose = pose    # Private tuple representing the position and orientation

    @property
    def elements(self):
        # Public getter for elements
        return self._elements

    @property
    def pose(self):
        # Public getter for pose
        return self._pose

    @pose.setter
    def pose(self, value):
        # Public setter for pose, allows updating the position and orientation
        self._pose = value

    def add_element(self, element):
        # Adds a new element or sub-assembly to the assembly
        self._elements.append(element)

    def to_json(self):
        # Convert assembly to a JSON-compatible format
        return {
            "elements": [element.to_json() for element in self._elements],
            "pose": self._pose
        }

    @staticmethod
    def from_json(data):
        # Create an Assembly instance from JSON data
        assembly = Assembly(data["pose"])
        for element_data in data["elements"]:
            element = Element.from_json(element_data)
            assembly.add_element(element)
        return assembly
