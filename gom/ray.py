# gom/ray.py
# Defines the Ray class for general optical models

import logging
from typing import List, Tuple
from gom.assembly import Assembly
from gom.parametric import distance, create_ray_segment, find_intersection


class Ray():
    def __init__(self, pose, power=1.0, max_length=1000, max_segments=10):
        # Initialize a ray with initial pose (origin) and max number of segments
        self.pose = pose                    # Tuple (x, y, orientation)
        self.power = power                  # Initialize the ray power        
        self.max_length = max_length        # Integer for max x, y coordinates
        self.max_segments = max_segments    # Integer for max number of ray segments
        self.type = 'ray'                   # 'ray'
        self.tkinter_id = None              # Add this line to store the TkInter ID of the element for rendering


    def trace_ray(self, assembly: 'Assembly') -> Tuple[List[Tuple[float, float, float]], List[float]]:
        '''
        Trace a ray through an assembly of elements
        Input: assembly (list of elements), self.ray_pose (x, y, angle)
        Output: ray_positions (list of (x, y, angle))
        '''
            
        # TODO boundry box with curved and complex elements - special assembly of 4 boundary elements
        # TODO ensure proper direction of the ray segment and separation from current element (avoid self-intersection)
        # TODO speed up the ray trace loop looking for the closest element intersection first: +1 / -1 over assembly

        # Log the start of the ray trace
        logging.info(f"Starting ray trace at {self.pose}")
        # Initialize the ray path with the initial pose and power
        self.ray_path = [self.pose]
        self.ray_power_path = [self.power]

        # Ray trace loop
        while True:
            # Initialize closest intersection point and intersected element
            closest_intersection = None
            closest_element = None
            closest_distance = None

            # Iterate over the elements in the assembly
            for element in assembly.elements:
                # Segment the ray pose (x,y,alpha) to parametric form (x,y,dx,dy)
                ray_segment = create_ray_segment(self.ray_path[-1], self.max_length)
                intersection = find_intersection(ray_segment, element.element_segment)
                # Find the closes intersecting element segment with the ray segment
                if intersection is not None:
                    distance_to_intersection = distance(self.ray_path[-1], intersection)
                    if closest_intersection is None or distance_to_intersection < closest_distance:
                        closest_intersection = intersection
                        closest_element = element
                        closest_distance = distance_to_intersection

            # Break the loop if no intersection is found or max length exceeded
            if closest_intersection is None or len(self.ray_path) >= self.max_segments:
                # No more intersections, break the loop
                break

            logging.debug(f"Closest intersection point: {closest_intersection}")
            # Make tuple of intersection point and ray angle
            incident_ray = (closest_intersection[0], closest_intersection[1], self.ray_path[-1][2])
            incident_power = self.ray_power_path[-1]
            # Trace the ray through the element with its method and add both to the ray path
            try:
                new_ray, new_power = closest_element.trace_ray(incident_ray, incident_power)
            except Exception as e:
                logging.error(f"Failed to trace ray through element: {e}")
                break
            # Add the incident and new ray to the ray_path and power_path
            self.ray_path.append(incident_ray)
            self.ray_path.append(new_ray)
            self.ray_power_path.append(incident_power)
            self.ray_power_path.append(new_power)
            # Log the incident and new ray and power
            logging.debug(f"Incident ray: {incident_ray}")
            logging.debug(f"New ray: {new_ray}")
            logging.debug(f"Incident power: {incident_power}")
            logging.debug(f"New power: {new_power}")

        # TODO Add final segment to the ray path to the scene boundary
        
        logging.info(f"Ray path: {self.ray_path}")
        logging.info(f"Ray power path: {self.ray_power_path}")
        return self.ray_path, self.ray_power_path


    # TODO speed up the ray trace loop looking for the closest element intersection first: +1 / -1 over assembly
    # TODO chenge this code in the trace_ray method above

    # # Get the current index
    # current_index = assembly.elements.index(closest_element) if closest_element else 0

    # # Iterate over the elements in the assembly in the desired order
    # for index in generate_indices(current_index, len(assembly.elements)):
    #     element = assembly.elements[index]

    # # New index generator for ray trace loop where the elements closest to the current one are checked first
    # def generate_indices(current_index, total_elements):
    #     yield current_index
    #     for i in range(1, total_elements):
    #         if current_index - i >= 0:
    #             yield current_index - i
    #         if current_index + i < total_elements:
    #             yield current_index + i