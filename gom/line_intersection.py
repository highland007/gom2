# Temporary test of Functions for finding the intersection of two lines.


import math

def ray_parametric_form(x0, y0, a):
    """
    Returns the parametric form coefficients of a ray given its origin and direction angle. 
    Input: x0, y0, a
    Output: x0, y0, dx, dy
    """
    rad = math.radians(a)
    return (x0, y0, math.cos(rad), math.sin(rad))


def find_ray_segment_intersection(ray, segment):
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
        print("Lines are parallel or coincident")
        return None  # No intersection (parallel or coincident lines)

    # Compute the parameter t for the intersection point on the ray
    t = ((xs - x0) * dys - (ys - y0) * dxs) / cross_product

    # Compute the parameter s for the intersection point on the segment
    s = ((xs - x0) * dy - (ys - y0) * dx) / cross_product

    # Debug output
    print(f"t: {t}, s: {s}")

    # Check if the intersection point is within the segment bounds (0 <= s <= 1)
    if 0 <= s <= 1:
        # Calculate the intersection point
        xi = x0 + t * dx
        yi = y0 + t * dy
        return (xi, yi)
    else:
        print("No intersection within the segment bounds")
        return None  # No intersection within the segment bounds

# Testing with a slightly modified example
# Ray: Origin (1, 2) with direction angle 45 degrees
ray = ray_parametric_form(1, 2, 0)
print(f"Ray: {ray}")

# Mirror Segment: Origin (3, 3) with direction angle 135 degrees and width 2
xm, ym, am, w = 3, 2, 0, 2
seg_start = ray_parametric_form(xm - w/2 * math.cos(math.radians(am + 90)), ym - w/2 * math.sin(math.radians(am + 90)), am)
seg_end = ray_parametric_form(xm + w/2 * math.cos(math.radians(am + 90)), ym + w/2 * math.sin(math.radians(am + 90)), am)
segment = (seg_start[0], seg_start[1], seg_end[0] - seg_start[0], seg_end[1] - seg_start[1])
print(f"Segment: {segment}")

# Find intersection with debug
intersection = find_ray_segment_intersection(ray, segment)
intersection

print(f"Intersection point: {intersection}")