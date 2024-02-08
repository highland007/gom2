# gom/ray.py
# Defines the Ray class for general optical models

import math
from gom.parametric import create_element_segment, create_ray_segment, find_intersection

class Ray():
    def __init__(self, pose, max_length=1000, max_segments=5):
        # Initialize a ray with initial pose (origin) and max number of segments
        self.pose = pose                    # Tuple (x, y, orientation)
        self.ray_path = [pose]              # List of ray segments (x, y, angle)
        self.max_length = max_length        # Integer for max x, y coordinates
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
        print(f"Starting ray trace at {self.pose}")

        # Iterate over the elements in the assembly
        for element in assembly.elements:

            # Segment the ray pose (x,y,alpha) to parametric form (x,y,dx,dy)
            ray_segment = create_ray_segment(self.ray_path[-1], self.max_length)
            print(f"Ray segment: {ray_segment}")

            # Find if the ray is intersecting the element or leaving the scene
            # TODO later with boundry box with curved and complex elements
            # TODO ensure proper direction of the ray segment and separation from current element (avoid self-intersection)
            # TODO scene bounday conditions
            # TODO improve the ray trace with the closest intersection
            intersection = find_intersection(ray_segment, element.element_segment)
            if intersection is not None:
                print(f"Intersection point: {intersection}")
                # Make tuple of intersection point and ray angle
                incident_ray = (intersection[0], intersection[1], self.ray_path[-1][2])
                # Trace the ray through the element with its method
                new_ray = element.trace_ray(incident_ray)
                # Add the incident and new ray to the ray_path
                self.ray_path.append(incident_ray)
                self.ray_path.append(new_ray)
                # Print the incident and new ray
                print(f"Incident ray: {incident_ray}")
                print(f"New ray: {new_ray}")

            # Break the loop if the max number of segments is reached
            if len(self.ray_path) >= self.max_segments:
                break

        # TODO Add final segment to the ray path to the scene boundary
        
        print(f"Ray path: {self.ray_path}")
        return self.ray_path
