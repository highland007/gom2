# gom/lens.py
# Defines the Lens class for general optical models

from gom.element import Element
from gom.parametric import calculate_refraction

class Lens(Element):
    def __init__(self, pose, size, refractive_index):
        super().__init__(pose, size, "lens")
        self.refractive_index = refractive_index

    # def trace_ray(self, ray, power):
    #   # TODO Implement the specific logic for tracing a ray through a lens