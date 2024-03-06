# gom/xtal.py
# Defines the Xtal class for general optical models

import math
from gom.element import Element
from gom.parametric import distance


class Xtal(Element):
    def __init__(self, pose, size, gain=2.0, acceptance=(10, 45)):
        super().__init__(pose, size, "xtal")
        self.gain = gain
        self.acceptance = acceptance

    def trace_ray(self, ray, power):
        # Unpack the crystal and ray poses, and acceptance variables
        xc, yc, ac = self.pose
        xr, yr, ar = ray[0], ray[1], ray[2]
        circle_of_acceptance = self.acceptance[0]
        angle_of_acceptance = self.acceptance[1]

        # Calculate the distance between the ray's position and the crystal's origin
        distance_xtal_ray = distance((xc, yc), (xr, yr))

        # Calculate the position overlap using a linear model
        if distance_xtal_ray <= circle_of_acceptance:
            position_overlap = 1 - (distance_xtal_ray / circle_of_acceptance)
        else:
            position_overlap = 0

        # Calculate the difference in angle between the ray's direction and the crystal's orientation
        angle_difference = abs(ar - ac)

        # Calculate the angle overlap using a cosine model
        if angle_difference < angle_of_acceptance:
            angle_overlap = math.cos(math.radians(angle_difference))
        else:
            angle_overlap = 0

        # The total gain is the product of the position overlap and the angle overlap
        total_gain = self.gain * position_overlap * angle_overlap

        # Multiply the power by the total gain
        new_power = power * total_gain

        # Shift the ray's position by a small amount to avoid self-intersection
        new_ray_x = ray[0] + self.epsilon
        new_ray_y = ray[1] + self.epsilon
        new_ray = (new_ray_x, new_ray_y, ray[2])
        # new_ray = ray

        return new_ray, new_power
