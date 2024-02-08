# gom/parametric.py
# Parametric line forms and calculations for optical ray tracing

import math

def parametric_form(pose):
    """
    Returns the parametric form coefficients of a line given its origin and direction angle. 
    Input: pose of ray or segment pose tuple (x, y, angle)
    Output: x0, y0, dx, dy
    """
    # Unpack the pose
    x0, y0, a = pose

    # Convert the angle to radians
    rad = math.radians(a)
        
    # Return the parametric form coefficients
    return (x0, y0, math.cos(rad), math.sin(rad))


def create_element_segment(pose, width):
    """
    Creates a segment given the midpoint, angle, and width.
    Input: pose (x, y, angle), size width of element
    Output: segment (xs, ys, dxs, dys)
    """
    # Unpack the pose and size
    xm, ym, am = pose
    w = width

    # Create the segment from the element pose and size (width)
    seg_start = parametric_form((xm - w/2 * math.cos(math.radians(am)), ym - w/2 * math.sin(math.radians(am)), am))
    seg_end = parametric_form((xm + w/2 * math.cos(math.radians(am)), ym + w/2 * math.sin(math.radians(am)), am))
        
    # Return the segment
    segment = (seg_start[0], seg_start[1], seg_end[0] - seg_start[0], seg_end[1] - seg_start[1])
    return segment
    

def create_ray_segment(pose, length):
    """
    Creates a segment given the starting point, angle, and length.
    Input: pose (x, y, angle), length of a ray segment
    Output: segment (xs, ys, dxs, dys)
    """
    # Unpack the pose and length
    x, y, angle = pose
    l = length

    # Calculate the ending point of the segment
    xe = x + l * math.cos(math.radians(angle))
    ye = y + l * math.sin(math.radians(angle))

    # Calculate the direction vector of the segment
    dx = xe - x
    dy = ye - y

    # Return the segment
    segment = (x, y, dx, dy)
    return segment


def find_intersection(segment1, segment2):
    """
    Finds the intersection point of a ray and a segment, with debug outputs.
    Input: ray, segment
    Output: intersection point (xi, yi)
    """
    # Unpack the ray and element segment parameters
    x0, y0, dx, dy = segment1
    xs, ys, dxs, dys = segment2

    # Check if the lines are parallel (cross product is zero)
    cross_product = dx * dys - dy * dxs
    if cross_product == 0:
        return None # No intersection (parallel or coincident lines)

    # Compute the parameter t for the intersection point on segment 1
    t = ((xs - x0) * dys - (ys - y0) * dxs) / cross_product

    # Compute the parameter s for the intersection point on segment 2
    s = ((xs - x0) * dy - (ys - y0) * dx) / cross_product

    # Check if the intersection point is within the segment bounds (0 <= s <= 1)
    if 0 <= s <= 1 and 0 <= t <= 1:
        # Calculate the intersection point
        xi = x0 + t * dx
        yi = y0 + t * dy
        return (xi, yi)
    else:
        return None  # No intersection within the segment bounds


def calculate_normal(segment):
    """ Calculate the normal vector to the segment. """
    _, _, dxs, dys = segment
    # Normal vector is perpendicular to the segment
    return dys, -dxs


def calculate_reflected_ray(ray, segment):
    """ Calculate the specular reflection of a ray on a mirror segment. """
    intersection = find_ray_segment_intersection(ray, segment)
    if intersection is None:
        return None  # No intersection, no reflection

    # Calculate the normal to the segment at the intersection point
    normal = calculate_normal(segment)
    nx, ny = normal

    # Ray direction
    _, _, dx, dy = ray

    # Normalize the normal vector
    norm_length = math.sqrt(nx**2 + ny**2)
    nx, ny = nx / norm_length, ny / norm_length

    # Dot product of ray direction and normal
    dot_product = dx * nx + dy * ny

    # Reflect the ray across the normal
    reflected_dx = dx - 2 * dot_product * nx
    reflected_dy = dy - 2 * dot_product * ny

    # Reflected ray starts at the intersection point
    reflected_ray_origin = intersection

    # Convert reflected direction into an angle
    reflected_angle = math.degrees(math.atan2(reflected_dy, reflected_dx))

    return reflected_ray_origin, reflected_angle
