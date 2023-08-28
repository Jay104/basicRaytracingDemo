import math
import cmath
from classes import *

# Calculate unit vector that starts at source and points toward dest
def get_unit_vector(source, dest):
    u_vect = vector (dest.x - source.x, dest.y - source.y, dest.z - source.z)
    magnitude = math.sqrt(u_vect.x ** 2 + u_vect.y ** 2 + u_vect.z ** 2)
    u_vect.x = u_vect.x / magnitude
    u_vect.y = u_vect.y / magnitude
    u_vect.z = u_vect.z / magnitude
    return u_vect

# Get the first object that is intersected (if any) by a ray drawn by u_vect_eye starting at eye_locat
def get_closest_object(eye_locat, u_vect_eye, object_list):

    t_vals = []

    # Calculate intersection point for each object in object_list
    for obj in object_list:
        t = complex(1, 1)

        # Finding the first intersection point for a sphere
        if (type(obj) is sphere):
            B = 2 * ((eye_locat.x - obj.center.x) * u_vect_eye.x + \
                    (eye_locat.y - obj.center.y) * u_vect_eye.y + \
                    (eye_locat.z - obj.center.z) * u_vect_eye.z)
            C = (eye_locat.x - obj.center.x) ** 2 + \
                (eye_locat.y - obj.center.y) ** 2 + \
                (eye_locat.z - obj.center.z) ** 2 - obj.radius ** 2
            t = (-1 * B - cmath.sqrt((B * B) - (4 * C))) / 2

        # The only other object in our list is the "wall"
        else:

            # The eye is positioned such that x > 0. If u_vect_eye is negative, then it will intersect the yz-plane
            if u_vect_eye.x < 0.0:
                t = (-1 * eye_locat.x) / u_vect_eye.x
                y_inter = eye_locat.y + (u_vect_eye.y * t)
                z_inter = eye_locat.z + (u_vect_eye.z * t)

                # Check if the y and z values are within that of the "wall"
                if y_inter < 0.0 or y_inter > 400.0 or z_inter > 0.0 or z_inter < -400.0:
                    t = complex(1, 1)
                else:
                    t = complex(t, 0)

        # If the ray intersects an object, then t should have no imaginery part
        if (t.imag == 0):
            t_vals.append([obj, t.real])

    closest_object = None

    if len(t_vals):
        t_vals = sorted(t_vals, key = lambda x:x[1])
        closest_object = t_vals[0]

    return closest_object