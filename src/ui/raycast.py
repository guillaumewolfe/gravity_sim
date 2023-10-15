import math 

def dot(v1,v2):
    return sum(a*b for a,b in zip(v1,v2))

def get_normalized_coordinates(x,y,width,heigh):
    normalized_x = (2.0*x)/width-1.0
    normalized_y = 1.0-(2.0*y)/heigh
    return normalized_x,normalized_y

def intersect(ray_origin,ray_direction,object_center,object_radius):
    oc = [ray_origin[i]-object_center[i] for i in range(3)]

    a = dot(ray_direction,object_center)
    b = 2.0*dot(oc,ray_direction)
    c = dot(oc,oc)-object_radius*object_radius

    discriminant = b*b-4*a*c
    return discriminant>0

def intersect_ray_sphere(ray_origin, ray_direction, sphere_center, sphere_radius):
    oc = [ray_origin[i] - sphere_center[i] for i in range(3)]

    a = sum([ray_direction[i]**2 for i in range(3)])
    b = 2 * sum([oc[i] * ray_direction[i] for i in range(3)])
    c = sum([oc[i]**2 for i in range(3)]) - sphere_radius**2

    discriminant = b**2 - 4*a*c
    if discriminant > 0:
        distance = (-b - math.sqrt(discriminant)) / (2.0*a)
        if distance > 0:
            return True, distance
    return False, float('inf')