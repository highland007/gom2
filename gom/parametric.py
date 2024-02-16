# gom/parametric.py
# Parametric segment math for optical ray tracing functions

# TODO rename to spatial.py for spatial math functions later
# TODO add real pose math for 2D and 3D, requires numpy (poetry)

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


def create_element_segment(element):
    """
    Creates a segment given the midpoint, angle, and width.
    Input: pose (x, y, angle), size width of element
    Output: segment (xs, ys, dxs, dys)
    """
    # Unpack the pose and size
    xm, ym, am = element.pose
    w, h = element.size

    # Create the segment from the element pose and size (width)
    seg_start = parametric_form((xm - w/2 * math.cos(math.radians(am + 90)), ym - w/2 * math.sin(math.radians(am + 90)), am))
    seg_end = parametric_form((xm + w/2 * math.cos(math.radians(am + 90)), ym + w/2 * math.sin(math.radians(am + 90)), am))
        
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


def calculate_reflection(ray, segment):
    """ Calculate the specular reflection of a ray on a mirror segment.
    Input: ray (x0, y0, dx, dy), segment (xs, ys, dxs, dys)
    Output: reflected_ray_origin (x, y), reflected_angle
    """
    # Calculate the normal to the element segment at the intersection point
    normal = calculate_normal(segment)
    nx, ny = normal

    # Calculate ray segment from the ray origin and a unit length
    ray_segment = create_ray_segment(ray, 1.0)

    # Ray direction
    _, _, dx, dy = ray_segment

    # Normalize the normal vector
    norm_length = math.sqrt(nx**2 + ny**2)
    nx, ny = nx / norm_length, ny / norm_length

    # Dot product of ray direction and normal
    dot_product = dx * nx + dy * ny

    # Reflect the ray across the normal
    reflected_dx = dx - 2 * dot_product * nx
    reflected_dy = dy - 2 * dot_product * ny

    # Convert reflected direction into an angle
    reflected_angle = math.degrees(math.atan2(reflected_dy, reflected_dx))

    return reflected_angle


# TODO REMOVE OLD used for element rendering for polygon in scene_renderer.py

def create_rotated_points(element):
        """
        Create a set of points for rotated rectangle.
        Input: x, y, angle, width, height
        Return: points Integer tuple
        """
        # Get coordinates and angle from the pose, assume (x, y, orientation)
        x, y, orientation = element.pose
        width, height = element.size
        # Calculate coordinates for the rectangle's corners without rotation (angle=0 degrees) facing right
        # Use "bellybutton" coordinates (center of the front face) as the origin
        x1 = x
        x2 = x - height
        y1 = y + width / 2
        y2 = y - width / 2
        # Create points representing the rectangle without rotation
        points = [x1, y1, x2, y1, x2, y2, x1, y2]
        # Rotate the points around the "bellybutton" and return the rotated points
        rotated_points = rotate_points(points, math.radians(orientation), (x,y))
        # Convert the rotated points to integers to avoid TkInter bug with float coordinates
        integer_points = [int(point) for point in rotated_points]
        return integer_points


def rotate_points(points, angle, center):
    """
    Rotate a point counter-clockwise by a given angle around a given origin.
    Input: points List, angle Float, center Tuple
    Output: points List
    """
    for i in range(0, len(points), 2):
        px, py = points[i], points[i+1]
        points[i] = math.cos(angle) * (px - center[0]) - math.sin(angle) * (py - center[1]) + center[0]
        points[i+1] = math.sin(angle) * (px - center[0]) + math.cos(angle) * (py - center[1]) + center[1]
    return points
