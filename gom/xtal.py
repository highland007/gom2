# gom/xtal.py
# Defines the Xtal class for general optical models

from gom.element import Element
# from gom.parametric import calculate_refraction

class Xtal(Element):
    def __init__(self, pose, size, gain=1.0):
        super().__init__(pose, size, "xtal")
        self.gain = gain

    def trace_ray(self, ray, power):
        # Simple Xtal model: just multiply the power by the gain
        new_ray = ray
        new_power = power * self.gain
        # TODO Implement the gain in a crystal from the incident ray position and angle
        """
        Prompt GHC: Can you help me implement the gain in the crystal with the following model?
        Gain is a function of the position and angle of the incident ray in the crystal
        Gain as function of positions is an overlap of two circles, one centered at (0, 0) and the other at (x, y)
        Gain as function of angle is gaussian with mean 0 and standard deviation is angle of acceptance
        """

        # TODO Later implement the specific logic for tracing a ray through a crystal
        return new_ray, new_power