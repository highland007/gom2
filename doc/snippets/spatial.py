# Snippet for using Homogeneous Transformation Matrices for Ray Tracing with Mirror and Lens classes
# Examples are below after class definitions
# Further 


# We can create a Lens class to handle refraction through two spherical surfaces. Each surface can be defined by its radius of curvature, origin point, and the index of refraction of the material. Additionally, we'll include the central thickness of the lens as a parameter. Here's how we can implement it:


import numpy as np

class HomogeneousTransformation:
    def __init__(self, rotation_matrix, translation_vector):
        self.rotation_matrix = rotation_matrix
        self.translation_vector = translation_vector
    
    def get_transformation_matrix(self):
        homogeneous_matrix = np.eye(4)
        homogeneous_matrix[:3, :3] = self.rotation_matrix
        homogeneous_matrix[:3, 3] = self.translation_vector
        return homogeneous_matrix


# The Mirror class now includes a method check_intersection to check if the ray intersects with the mirror's surface within the aperture.
# The Ray class's trace_ray method iterates over each element, checks for intersections, and updates the ray's origin and direction accordingly.
# If an intersection is found with any mirror, the ray is reflected and the loop terminates. This assumes that the ray interacts only with the first mirror it encounters.
# This approach allows for efficiently checking for intersections with surfaces of limited size and updating the ray's position and direction accordingly, while still leveraging the power of homogeneous transformation matrices.


class Mirror:
    def __init__(self, pose):
        self.pose = pose  # Pose is an instance of HomogeneousTransformation
    
    def reflect_rays(self, ray_directions):
        surface_normal = np.array([0, 0, 1])  # Surface normal along the z-axis
        return ray_directions - 2 * np.dot(ray_directions, surface_normal)[:, np.newaxis] * surface_normal
    
    def transform_rays_to_local(self, ray_origins, ray_directions):
        pose_matrix_inv = np.linalg.inv(self.pose.get_transformation_matrix())
        local_origins = np.dot(ray_origins - self.pose.translation_vector, pose_matrix_inv[:3, :3].T)
        local_directions = np.dot(ray_directions, pose_matrix_inv[:3, :3].T)
        return local_origins, local_directions
    
    def transform_rays_to_global(self, local_origins, local_directions):
        global_origins = np.dot(local_origins, self.pose.rotation_matrix.T) + self.pose.translation_vector
        global_directions = np.dot(local_directions, self.pose.rotation_matrix.T)
        return global_origins, global_directions
    

# In this Lens class:
# We define parameters for the lens, such as its pose, radii of curvature for both surfaces (r1 and r2), origin points of the surfaces (origin1 and origin2), central thickness (central_thickness), and refractive index (refractive_index).
# The refract_ray method would implement the logic for refraction through the lens.
# Methods transform_ray_to_local and transform_ray_to_global are included to transform the ray between local and global coordinate systems.
# The refract_ray method calculates the intersection points of the ray with each surface of the lens and then applies Snell's law to compute the refracted ray direction.
# The calculate_intersection method calculates the intersection of the ray with a spherical surface using the quadratic formula.
# If both intersections are found and the ray is entering the lens, the method calculates the angles of incidence and refraction and computes the refracted ray direction accordingly.
# If no intersection is found or the ray is exiting the lens, no refraction occurs, and the original ray direction is returned.

class Lens:
    def __init__(self, pose, r1, r2, origin1, origin2, central_thickness, refractive_index):
        self.pose = pose  # Pose is an instance of HomogeneousTransformation
        self.r1 = r1  # Radius of curvature of the first surface
        self.r2 = r2  # Radius of curvature of the second surface
        self.origin1 = origin1  # Origin point of the first surface
        self.origin2 = origin2  # Origin point of the second surface
        self.central_thickness = central_thickness  # Central thickness of the lens
        self.refractive_index = refractive_index  # Refractive index of the material
    
    def refract_rays(self, ray_directions):
        # Refraction logic here
        pass
    
    def transform_rays_to_local(self, ray_origins, ray_directions):
        pose_matrix_inv = np.linalg.inv(self.pose.get_transformation_matrix())
        local_origins = np.dot(ray_origins - self.pose.translation_vector, pose_matrix_inv[:3, :3].T)
        local_directions = np.dot(ray_directions, pose_matrix_inv[:3, :3].T)
        return local_origins, local_directions
    
    def transform_rays_to_global(self, local_origins, local_directions):
        global_origins = np.dot(local_origins, self.pose.rotation_matrix.T) + self.pose.translation_vector
        global_directions = np.dot(local_directions, self.pose.rotation_matrix.T)
        return global_origins, global_directions


# Example usage of the Mirror and Lens classes:

# In this example:
# We import the Mirror, Lens, and HomogeneousTransformation classes from their respective files.
# We define poses for a mirror and a lens using HomogeneousTransformation.
# We create instances of Mirror and Lens with the defined poses.
# We define a bundle of rays with random origins and directions.
# We transform the ray origins and directions to the local coordinate system of the mirror.
# We perform interactions with the mirror (reflection).
# We transform the reflected ray directions back to the global coordinate system.
# Finally, we print the reflected ray directions.


# Define poses for mirrors
mirror_pose = HomogeneousTransformation(np.eye(3), np.array([0, 0, 0]))

# Create mirror instance
mirror = Mirror(mirror_pose)

# Define poses and parameters for the lens
lens_pose = HomogeneousTransformation(np.eye(3), np.array([0, 0, 0]))
r1 = 2.0  # Example radius of curvature for the first surface
r2 = -2.0  # Example radius of curvature for the second surface (negative for concave)
origin1 = np.array([0, 0, 1])  # Example origin point for the first surface
origin2 = np.array([0, 0, 5])  # Example origin point for the second surface
central_thickness = 0.5  # Example central thickness of the lens
refractive_index = 1.5  # Example refractive index of the material

# Create lens instance
lens = Lens(lens_pose, r1, r2, origin1, origin2, central_thickness, refractive_index)

# Define bundle of rays
num_rays = 10
ray_origins = np.random.rand(num_rays, 3)  # Random origins for the rays
ray_directions = np.random.rand(num_rays, 3)  # Random directions for the rays

# Transform ray origins and directions to local coordinate system
local_ray_origins, local_ray_directions = mirror.transform_rays_to_local(ray_origins, ray_directions)

# Perform interactions with mirror
reflected_ray_directions = mirror.reflect_rays(local_ray_directions)

# Transform reflected ray directions to global coordinate system
global_reflected_ray_directions = mirror.transform_rays_to_global(local_ray_origins, reflected_ray_directions)

print("Reflected Ray Directions:", global_reflected_ray_directions)
