# gom/xtal.py
# Defines the Xtal class for general optical models

from gom.element import Element
from gom.parametric import calculate_refraction

class Xtal(Element):
    def __init__(self, pose, size, some_property):
        super().__init__(pose, size, "xtal")
        self.some_property = some_property

    # def trace_ray(self, ray, power):
    #     # TODO Implement the specific logic for tracing a ray through a xtal