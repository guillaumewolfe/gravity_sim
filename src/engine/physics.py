import sys
import os 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.ui import celestial_objects as CO
import math

def update_accel(obj, objects, dt):
    G = 6.67430e-11  # Constante gravitationnelle en m^3⋅kg^−1⋅s^−2

    total_accel = [0, 0, 0]  # Accélération totale due à la gravité de tous les autres objets
    
    for other_obj in objects:
        if obj.name != other_obj.name:
            # Calculer le vecteur directionnel entre obj et other_obj
            vector_direction = [other_pos - obj_pos for other_pos, obj_pos in zip(other_obj.real_position, obj.real_position)]
            distance = math.sqrt(sum(coord ** 2 for coord in vector_direction))
            
            # Normaliser le vecteur directionnel
            unit_vector = [coord / distance for coord in vector_direction]
            
            # Calculer l'accélération due à la gravité entre obj et other_obj
            accel_magnitude = G * other_obj.weight / distance**2
            accel_vector = [unit * accel_magnitude for unit in unit_vector]
            
            # Ajouter cette accélération à l'accélération totale
            total_accel = [total + accel for total, accel in zip(total_accel, accel_vector)]
            
    obj.accel = total_accel





def update_vitesse(obj,dt):
    correction = 1
    obj.velocity = [elem+obj.accel[index]*dt*correction for index,elem in enumerate(obj.velocity)]

def update_positions(obj, dt):
    # mise à jour de la position réelle
    obj.real_position = [obj.real_position[i] + obj.velocity[i] * dt for i in range(3)]
    
    # mise à jour de la position de simulation (mise à l'échelle)
    obj.position_simulation = [CO.SimulationScale.to_distance(coord) for coord in obj.real_position]

    append_position_history(obj)


def append_position_history(obj):
    obj.update_distance_list()
    distance = obj.calculate_distance_parcourue()
    if obj.name=="Terre":
        print(len(obj.position_history))
    if distance > obj.demi_orbite:
        obj.position_history.pop(0)
    obj.position_history.append(obj.position_simulation)

def update_rotation(obj,dt):
    obj.rotation_siderale_angle += obj.rotation_siderale_vitesse*dt
    obj.rotation_siderale_angle = obj.rotation_siderale_angle%360

    
def update_physics(objects, dt):

    for obj in objects:
        update_rotation(obj,dt)
        #if obj.name=="Terre": print(len(obj.position_history))
        if obj.name!=obj.relation:
            #if obj.name=="Soleil": print(obj.rotation_siderale_angle)
            update_accel(obj,objects,dt)
            update_vitesse(obj,dt)
            update_positions(obj,dt)
        
