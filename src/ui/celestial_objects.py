from pyglet.gl import *
import math

class SimulationScale:
    DISTANCE_SCALE = 1e7  
    SIZE_MIN = 0.01  # Rayon minimum dans la simulation
    SIZE_MAX = 1.5     # Rayon maximum (pour le Soleil)

    @classmethod
    def to_distance(cls, real_distance):
        return real_distance / cls.DISTANCE_SCALE

    @classmethod
    def to_size(cls, real_radius):
        # Mise à l'échelle logarithmique
        scaled_size = math.log(real_radius + 1)
        max_radius_real = 3390
        # Normalisation: ajuster la taille mise à l'échelle pour qu'elle se situe entre SIZE_MIN et SIZE_MAX
        min_log_scale = math.log(1 + 1)  # Plus petite valeur possible après mise à l'échelle logarithmique (1 pour éviter le log de 0)
        max_log_scale = math.log(max_radius_real + 1)  # Plus grande valeur (rayon du Soleil)
        normalized_size = cls.SIZE_MIN + (scaled_size - min_log_scale) / (max_log_scale - min_log_scale) * (cls.SIZE_MAX - cls.SIZE_MIN)
        
        return normalized_size

class CelestialObject:
    def __init__(self, name, relation, position, size, texture_path, velocity=None, force=None,accel=None,weight=None, real_radius=None, real_distance=None):
        self.name = name
        self.size=size
        self.position = position
        self.relation = relation
        self.texture = pyglet.image.load(texture_path).get_texture()
        self.velocity = velocity or [0, 0, 0]
        self.force = force or [0, 0, 0]
        self.accel = accel or [0,0,0]
        self.weight = weight or 0
        
        # Use simulation scales
        if real_distance is not None:
            self.distance_origine = SimulationScale.to_distance(real_distance)
        else:
            self.distance_origine = position  # assume position is already in simulation units if real_distance is not provided
        
        if real_radius is not None:
            self.radius = SimulationScale.to_size(real_radius)
        else:
            self.radius = size  # assume size is already in simulation units if real_radius is not provided

CELESTIAL_PARAMETERS = [
    {
        "name": "Soleil",
        "relation": "Soleil",
        "real_distance": 0,
        "real_radius": 696_340,
        "weight": 1.989e30,
        "velocity": [0, 0, 0],
        "accel":[0,0,0],
        "texture_path": "assets/textures/sun.jpg"
    },
    {
        "name": "Terre",
        "relation": "Soleil",
        "real_distance": 149_597_870,
        "real_radius": 6371,
        "weight": 5.972e24,
        "velocity": [0, 0.4, 0],
        "accel":[0,0,0],
        "texture_path": "assets/textures/earth_real.jpg"
    },
    {
        "name": "Lune",
        "relation": "Terre",
        "real_distance": 3844000*7.5,
        "real_radius": 10,
        "weight": 7.342e22,
        "velocity": [0, 0.0, 0],
        "accel":[0,0,0],
        "texture_path": "assets/textures/lunar.jpg"
    },
    {
        "name": "Mars",
        "relation": "Soleil",
        "real_distance": 225_000_000,
        "real_radius": 3390,
        "weight": 6.417e23,
        "velocity": [0, 1.3, 0],
        "accel":[0,0,0],
        "texture_path": "assets/textures/mars.jpg"
    }
]

def create_celestial_objects(params_list):
    objects = []
    for params in CELESTIAL_PARAMETERS:
        if params["relation"] == params["name"]:  # Si l'objet est son propre point de référence (comme le Soleil)
            position = [0, 0, 0]
        else:
            # Trouver l'objet de référence dans la liste des objets déjà créés
            reference_obj = next(obj for obj in objects if obj.name == params["relation"])
            # Placer l'objet à la distance réelle de l'objet de référence sur l'axe des x
            position = [reference_obj.position[0] + SimulationScale.to_distance(params["real_distance"]), 0, 0]
        
        obj = CelestialObject(
            name=params["name"],
            relation=params["relation"],
            position=position,
            size=SimulationScale.to_size(params["real_radius"]),
            texture_path=params["texture_path"],
            velocity=params["velocity"],
            weight=params["weight"],
            accel=params["accel"]
        )
        objects.append(obj)
    return objects