# gom/base.py
# Defines the base class for common methods like to_json and from_json

class Serializable:
    def to_json(self):
        # Convert the object to a JSON-compatible format
        raise NotImplementedError("to_json method must be implemented in the derived class")

    @staticmethod
    def from_json(data):
        # Create an instance of the class from JSON data
        raise NotImplementedError("from_json method must be implemented in the derived class")
