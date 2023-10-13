from pyglet.gl import *
import math
from objectCelesteData import CELESTIAL_PARAMETERS



class CelestialObject:
    def __init__(self, name, relation, real_position, real_radius, texture_path,position_simulation=None,rayon_simulation=None ,velocity=None, force=None, accel=None, weight=None,inclinaison=None,rotation_siderale_angle=None,rotation_siderale_vitesse=None,rotation_direction=None):
        self.name = name
        self.real_position = real_position  # position en unités réelles
        self.relation = relation
        self.texture = pyglet.image.load(texture_path).get_texture()
        self.velocity = velocity or [0, 0, 0]
        self.force = force or [0, 0, 0]
        self.accel = accel or [0, 0, 0]
        self.weight = weight or 0
        self.real_radius = real_radius  # rayon en unités réelles
        self.position_simulation = position_simulation or [0,0,0]
        self.rayon_simulation = rayon_simulation or 0.0001
        self.inclinaison = inclinaison or 0
        self.rotation_siderale_angle = rotation_siderale_angle or 0
        self.rotation_siderale_vitesse = rotation_siderale_vitesse or 0
        self.rotation_direction = rotation_direction or [0,0,0]


def create_celestial_objects(params_list):
    objects = []
    
    for params in params_list:
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
            texture_path=params["texture_path"],
            velocity=params["velocity"],
            weight=params["weight"],
            accel=params["accel"],
            inclinaison=params["inclinaison"],
            rotation_siderale_angle=params["rotation_siderale_angle"],
            rotation_siderale_vitesse=params["rotation_siderale_vitesse"],
            rotation_direction=params["rotation_siderale_direction"],
            position_simulation=position_simulation,
            rayon_simulation=rayon_simulation
        )
        
        objects.append(obj)
    return objects





distanceTerreSoleil = 149_597_870e3
facteur = 7.5
SCALE = distanceTerreSoleil/facteur


class SimulationScale:
    DISTANCE_SCALE = SCALE
    SIZE_MIN = 0.5  # Rayon minimum dans la simulation
    SIZE_MAX = 2    # Rayon maximum (pour le Soleil)

    @classmethod
    def to_distance(cls, real_distance):
        return real_distance / cls.DISTANCE_SCALE

    @classmethod
    def to_size(cls, real_radius):
        # Mise à l'échelle linéaire
        max_radius_real = 696_340e3  # Rayon du Soleil en km
        min_radius_real = 2439.7e3  # Supposons qu'il s'agisse d'un rayon minimum réaliste pour un petit objet

        # Interpolation linéaire entre SIZE_MIN et SIZE_MAX
        normalized_size = cls.SIZE_MIN + (real_radius - min_radius_real) / (max_radius_real - min_radius_real) * (cls.SIZE_MAX - cls.SIZE_MIN)
        
        return normalized_size
