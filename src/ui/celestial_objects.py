from pyglet.gl import *
import math
from objectCelesteData import CELESTIAL_PARAMETERS



class CelestialObject:
    def __init__(self, name, texture, real_radius = 6371e3,texture_isLoaded = False ,real_position = [0,0,0], relation = None, type_object = 2, real_distance = 0,position_simulation=None,rayon_simulation=None ,velocity=None, force=None, accel=None, weight=None,inclinaison=None,rotation_siderale_angle=None,rotation_siderale_vitesse=None,rotation_direction=None,color_id = (0,0,0)):
        self.name = name
        self.real_position = real_position  # position en unités réelles
        self.relation = relation
        if not texture_isLoaded:
            self.texture = pyglet.image.load(texture).get_texture()
        else:
            self.texture = texture
        self.velocity = velocity or [0, 0, 0]
        self.force = force or [0, 0, 0]
        self.accel = accel or [0, 0, 0]
        self.type_object = type_object
        self.weight = weight or 0
        self.real_radius = real_radius  # rayon en unités réelles
        self.real_distance = real_distance or 0
        self.position_simulation = position_simulation or [0,0,0]
        self.rayon_simulation = rayon_simulation or 0.0001
        self.inclinaison = inclinaison or 0
        self.rotation_siderale_angle = rotation_siderale_angle or 0
        self.rotation_siderale_vitesse = rotation_siderale_vitesse or 0
        self.rotation_direction = rotation_direction or [0,0,0]
        self.color_id = color_id or (0,0,0)
        self.position_history = []
        self.max_position_history = 500
        self.drawOrbitEnable = True
        self.distance_list = []
        self.demi_orbite = math.pi * SimulationScale.to_distance(real_distance)/1.25
    
    def update_distance_list(self):
        if len(self.position_history)>2:
            def distance(p1, p2):
                return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)**0.5
        
            self.distance_list = [distance(self.position_history[i], self.position_history[i+1]) for i in range(len(self.position_history)-1)]

    def calculate_distance_parcourue(self):
        if len(self.distance_list) == 0: return 0
        return sum(self.distance_list)
    def get_velocity(self):
        return (self.velocity[0]**2+self.velocity[1]**2+self.velocity[2]**2)**(0.5)
    
    def get_force(self):
        accel_n = (self.accel[0]**2+self.accel[1]**2+self.accel[2]**2)**(0.5)
        return accel_n * self.weight


def create_celestial_objects(params_list):
    objects = []
    
    for index,params in enumerate(params_list):
        # Déterminez la position réelle
        if params["relation"] == params["name"]:  # Si l'objet est son propre point de référence (comme le Soleil)
            real_position = [0, 0, 0]
        else:
            # Trouvez l'objet de référence dans la liste des objets déjà créés
            reference_obj = next(obj for obj in objects if obj.name == params["relation"])
            # Placez l'objet à la distance réelle de l'objet de référence sur l'axe des x
            real_position = [reference_obj.real_position[0] + params["real_distance"], 0, 0]
        
        # Calculer la position et le rayon pour la simulation (affichage)
        position_simulation = [SimulationScale.to_distance(coord) for coord in real_position]
        rayon_simulation = SimulationScale.to_size(params["real_radius"])
        
        # Créez l'objet céleste
        obj = CelestialObject(
            name=params["name"],
            relation=params["relation"],
            real_position=real_position,
            real_radius=params["real_radius"],
            texture=params["texture_path"],
            velocity=params["velocity"],
            weight=params["weight"],
            accel=params["accel"],
            type_object=params["type"],
            real_distance=params["real_distance"],
            inclinaison=params["inclinaison"],
            rotation_siderale_angle=params["rotation_siderale_angle"],
            rotation_siderale_vitesse=params["rotation_siderale_vitesse"],
            rotation_direction=params["rotation_siderale_direction"],
            position_simulation=position_simulation,
            rayon_simulation=rayon_simulation,
            color_id=generate_color_id(index)
        )
        
        objects.append(obj)
    return objects


def generate_color_id(index):
    r_val = (index//10)*25
    g_val = (index%10)*25
    return (r_val,g_val,0)


distanceTerreSoleil = 149_597_870e3
facteur = 25
SCALE = distanceTerreSoleil/facteur


class SimulationScale:
    DISTANCE_SCALE = SCALE
    SIZE_MIN = 1  # Rayon minimum dans la simulation
    SIZE_MAX = 4   # Rayon maximum (pour le Soleil)

    # ... Vos autres méthodes ici ...

    @classmethod
    def to_distance(cls, real_distance):
        return real_distance / cls.DISTANCE_SCALE

    @classmethod
    def to_size(cls, real_radius):
        if real_radius == 696_340e3:
            return 6
       
        # Mise à l'échelle linéaire
        max_radius_real = 69911e3  # Rayon de Jupiter
        min_radius_real = 1737.5e3  # Supposons qu'il s'agisse d'un rayon minimum réaliste pour un petit objet

        # Interpolation linéaire entre SIZE_MIN et SIZE_MAX
        normalized_size = cls.SIZE_MIN + (real_radius - min_radius_real) / (max_radius_real - min_radius_real) * (cls.SIZE_MAX - cls.SIZE_MIN)
       
        return normalized_size

    @classmethod
    def from_distance(cls, scaled_distance):
        return scaled_distance * cls.DISTANCE_SCALE

    @classmethod
    def from_size(cls, normalized_size):
        max_radius_real = 69911e3
        min_radius_real = 1737.5e3

        real_radius = min_radius_real + (normalized_size - cls.SIZE_MIN) / (cls.SIZE_MAX - cls.SIZE_MIN) * (max_radius_real - min_radius_real)

        return real_radius



