# gom/lens.py
# Defines the Lens class for general optical models

from gom.element import Element
from gom.parametric import calculate_refraction


class Lens(Element):
    def __init__(self, pose, size, focal_length):
        super().__init__(pose, size, "lens")
        self.focal_length = focal_length
        # TODO Refractive index of the lens material not used for thin lens approximation
        # self.refractive_index = refractive_index

    def trace_ray(self, ray, power):
        # TODO move calculate_refraction here or leave at parametric.py?
        new_ray = calculate_refraction(
            ray, self.pose, self.element_segment, self.focal_length)
        new_power = power
        return new_ray, new_power
