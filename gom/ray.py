# gom/ray.py
# Defines the Ray class for general optical models

import math

class Ray():
    def __init__(self, pose, max_segments=100):
        # Initialize a ray with initial pose (origin) and max number of segments
        self.pose = pose                    # Tuple (x, y, orientation)
        self.max_segments = max_segments    # Integer
        self.type = 'ray'                   # 'ray'
        self.tkinter_id = None              # Add this line to store the TkInter ID of the element for rendering

    def trace_ray(self, assembly):
        '''
        Trace a ray through an assembly of elements
        Input: assembly (list of elements), self.ray_pose (x, y, angle)
        Output: ray_positions (list of (x, y, angle))
        '''
        # Start with the initial ray position
        ray_positions = [self.pose[:2]]

        # Convert the ray to parametric form
        ray_parametric = self.parametric_form(self.pose[0], self.pose[1], self.pose[2])

        # Iterate over the elements in the assembly
        for element in assembly:
            # Segment the element into a list of starting and end points (x, y)
            segment = self.create_segment(element.pose[0], element.pose[1], element.pose[2], element.size[0])
            # Find if the ray is intersecting the element
            intersection = self.find_ray_segment_intersection(ray_parametric, segment)
            # Trace the ray through the element
            self.pose = element.trace_ray(self.pose)
            # Add the new ray position to the list
            ray_positions.append(self.pose[:2])


    # Create a ray given its origin and direction angle
    def parametric_form(x0, y0, a):
        """
        Returns the parametric form coefficients of a ray given its origin and direction angle. 
        Input: x0, y0, a
        Output: x0, y0, dx, dy
        """
        rad = math.radians(a)
        return (x0, y0, math.cos(rad), math.sin(rad))

    # Create a segment given the midpoint, angle, and width.
    def create_segment(xm, ym, am, w):
        """
        Creates a segment given the midpoint, angle, and width.
        Input: xm, ym, am, w
        Output: segment (xs, ys, dxs, dys)
        """
        seg_start = self.parametric_form(xm - w/2 * math.cos(math.radians(am)), ym - w/2 * math.sin(math.radians(am)), am)
        seg_end = self.parametric_form(xm + w/2 * math.cos(math.radians(am)), ym + w/2 * math.sin(math.radians(am)), am)
        segment = (seg_start[0], seg_start[1], seg_end[0] - seg_start[0], seg_end[1] - seg_start[1])
        return segment

    # Find the intersection point of a ray and a segment
    def ray_segment_intersection(ray, segment):
        """
        Finds the intersection point of a ray and a segment, with debug outputs.
        Input: ray, segment
        Output: intersection point (xi, yi)
        """
        # Unpack the ray and segment parameters
        x0, y0, dx, dy = ray
        xs, ys, dxs, dys = segment

        # Check if the lines are parallel (cross product is zero)
        cross_product = dx * dys - dy * dxs
        if cross_product == 0:
            return None # No intersection (parallel or coincident lines)

        # Compute the parameter t for the intersection point on the ray
        t = ((xs - x0) * dys - (ys - y0) * dxs) / cross_product

        # Compute the parameter s for the intersection point on the segment
        s = ((xs - x0) * dy - (ys - y0) * dx) / cross_product

        # Check if the intersection point is within the segment bounds (0 <= s <= 1)
        if 0 <= s <= 1:
            # Calculate the intersection point
            xi = x0 + t * dx
            yi = y0 + t * dy
            return (xi, yi)
        else:
            return None  # No intersection within the segment bounds
