from PIL import Image
import math
import cmath
from classes import *
from functions import *

img_height = 400
img_width = 400

img = Image.new('RGB', (img_width, img_height))
pixels = img.load()
for i in range(img_height):
    for j in range(img_width):
        pixels[(i, j)] = (50, 50, 50)

light_color = RGB_float (1.0, 1.0, 1.0)
light_locat = point (img_width, img_height // 2, (img_height // 8) * -1)

mid = img_height // 2
eye_locat = point(mid, mid, mid)

sphere1 = sphere (point (125, 150, -150), \
                  75, \
                  RGB_float(0.5, 0.0, 0.5))
sphere2 = sphere (point (220, 210, -95), \
                  40, \
                  RGB_float(0.0, 0.5, 0.5))
plane = [[0, 0, 0], [0, img_height, img_width * -1]]
object_list = [plane, sphere1, sphere2]
K = 0.5

for i in range (img_width):
    for j in range (img_height):    # For each pixel in the image

        # Calculate unit vector from eye_locat to pixel i, j
        dest = point (i, j, 0)
        u_vect_eye = get_unit_vector(eye_locat, dest)

        # Get location of closest object (if any) in line with the unit vector
        e_closest_object = get_closest_object(eye_locat, u_vect_eye, object_list)
    
        # There is an object in the direction of u_vect_eye --> use lighting model
        if e_closest_object is not None:

            t1 = e_closest_object[1]
            x = eye_locat.x + (u_vect_eye.x * t1)
            y = eye_locat.y + (u_vect_eye.y * t1)
            z = eye_locat.z + (u_vect_eye.z * t1)
            # print("- before get_closest_object xyz: ", x, y, z)
            dest = point (x, y, z)

            # Calculate unit vector from light_locat to first object intersected by u_eye
            u_vect_light = get_unit_vector(light_locat, dest)

            # Get location of closest object (if any) in line with the unit vector
            l_closest_object = get_closest_object(light_locat, u_vect_light, object_list)

            # The eye and light source see the same object --> calculate color
            if l_closest_object is not None and e_closest_object[0] is l_closest_object[0]:

                # Calculate color of object
                if type(e_closest_object[0]) is sphere:

                    # Calculate normal vector of sphere's surface at point (x, y, z)
                    cur_sphere = e_closest_object[0]
                    norm_vect = vector (x - cur_sphere.center.x, y - cur_sphere.center.y, z - cur_sphere.center.z)
                    magnitude = math.sqrt(norm_vect.x ** 2 + norm_vect.y ** 2 + norm_vect.z ** 2)
                    norm_vect.x = norm_vect.x / magnitude
                    norm_vect.y = norm_vect.y / magnitude
                    norm_vect.z = norm_vect.z / magnitude

                    # Find cos(A), or the dot product, of the normal vector and unit vector from the light source
                    dot_prod = (norm_vect.x * u_vect_light.x + norm_vect.y * u_vect_light.y + norm_vect.z * u_vect_light.z) * -1
                    dot_prod = max(dot_prod, 0)     # If the result is less than 0, set to 0

                    r = cur_sphere.color.r * light_color.r * dot_prod
                    g = cur_sphere.color.g * light_color.g * dot_prod
                    b = cur_sphere.color.b * light_color.b * dot_prod
                    r = int(r * 256)
                    g = int(g * 256)
                    b = int(b * 256)
                    pixels[(i, j)] = (r, g, b)

                # For the plane in this project, its normal vector is in the positive x direction with magnitude of 1
                else:
                    norm_vect = vector(1, 0, 0)

                    dot_prod = (norm_vect.x * u_vect_light.x + norm_vect.y * u_vect_light.y + norm_vect.z * u_vect_light.z) * -1
                    dot_prod = max(dot_prod, 0)     # If the result is less than 0, set to 0

                    r = 75 * light_color.r * dot_prod
                    g = 75 * light_color.g * dot_prod
                    b = 75 * light_color.b * dot_prod
                    r = int(r * 256)
                    g = int(g * 256)
                    b = int(b * 256)
                    pixels[(i, j)] = (r, g, b)

            # The eye and light source don't see the same object --> shadow
            else:
                pixels[(i, j)] = (0, 0, 0)


img.show()

