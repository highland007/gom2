# gom/ray.py
# Defines the Ray class for general optical models

import math

class Ray():
    def __init__(self, pose, max_coords=600, max_segments=5):
        # Initialize a ray with initial pose (origin) and max number of segments
        self.pose = pose                    # Tuple (x, y, orientation)
        self.ray_path = [pose]              # List of ray segments (x, y, angle)
        self.max_coords = max_coords        # Integer for max x, y coordinates
        self.max_segments = max_segments    # Integer for max number of ray segments
        self.type = 'ray'                   # 'ray'
        self.tkinter_id = None              # Add this line to store the TkInter ID of the element for rendering

    def trace_ray(self, assembly):
        '''
        Trace a ray through an assembly of elements
        Input: assembly (list of elements), self.ray_pose (x, y, angle)
        Output: ray_positions (list of (x, y, angle))
        '''
        # Restart with the initial ray pose on every trace
        self.ray_path = [self.pose]

        # Trace the ray through the assembly or until the max number of segments is reached
        for _ in range(self.max_segments):
            if len(self.ray_path) >= self.max_segments:
                break

            # Iterate over the elements in the assembly
            for element in assembly:

                # Convert the curent ray segment pose (x,y,alpha) to parametric form (x,y,dx,dy)
                ray_segment = self.parametric_form(self.ray_path[-1])

                # Segment the element (pose, width) into parametric form (x,y,dx,dy)
                element_segment = self.create_segment(element.pose, element.size)

                # Find if the ray is intersecting the element
                intersection = self.find_intersection(ray_segment, element_segment)
                if intersection is not None:
                    # Make tupe of intersection point and ray angle
                    incident_ray = (intersection[0], intersection[1], self.ray_path[-1][2])
                    # Add the intersection point to the ray_path
                    self.ray_path.append(incident_ray)
                    # Trace the ray through the element with its method
                    new_ray = element.trace_ray(self.ray_path[-1])
                    # Add the new ray to the ray_path
                    self.ray_path.append(new_ray)

                # TODO scene bounday conditions
                # TODO improve the ray trace with the closest intersection
        
        return self.ray_path


    def parametric_form(self, pose):
        """
        Returns the parametric form coefficients of a ray given its origin and direction angle. 
        Input: pose of ray or segment pose tuple (x, y, angle)
        Output: x0, y0, dx, dy
        """
        # Unpack the pose
        x0, y0, a = pose

        # Convert the angle to radians
        rad = math.radians(a)
        
        # Return the parametric form coefficients
        return (x0, y0, math.cos(rad), math.sin(rad))


    def create_segment(self, pose, size):
        """
        Creates a segment given the midpoint, angle, and width.
        Input: pose (x, y, angle), size (width, height) of element
        Output: segment (xs, ys, dxs, dys)
        """
        # Unpack the pose and size
        xm, ym, am = pose
        w = size[0]

        # Create the segment from the element pose and size (width)
        seg_start = self.parametric_form((xm - w/2 * math.cos(math.radians(am)), ym - w/2 * math.sin(math.radians(am)), am))
        seg_end = self.parametric_form((xm + w/2 * math.cos(math.radians(am)), ym + w/2 * math.sin(math.radians(am)), am))
        
        # Return the segment
        segment = (seg_start[0], seg_start[1], seg_end[0] - seg_start[0], seg_end[1] - seg_start[1])
        return segment


    def find_intersection(self, ray, segment):
        """
        Finds the intersection point of a ray and a segment, with debug outputs.
        Input: ray, segment
        Output: intersection point (xi, yi)
        """
        # Unpack the ray and element segment parameters
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
