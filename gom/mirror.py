# gom/mirror.py
# Defines the Mirror class for general optical models

from gom.element import Element
from gom.parametric import calculate_reflection

class Mirror(Element):
    def __init__(self, pose, size, reflectivity=1.0):
        super().__init__(pose, size, "mirror")
        self.reflectivity = reflectivity

    def trace_ray(self, ray, power):
        new_ray = calculate_reflection(ray, self.element_segment)
        new_power = power * self.reflectivity
        return new_ray, new_power