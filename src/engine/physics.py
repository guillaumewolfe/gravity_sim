import sys
import os 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.ui import celestial_objects as CO
import math

def update_accel(obj,objects,dt):
    G = 10**(-32)
    #Touver l'object en relation
    object_relation = None
    for o in objects:
        if obj.relation == o.name:
            object_relation = o
    
    #Distance = math.sqrt((x_obj1-x_obj2)**2+(y_obj1-y_obj2)**2+(y_obj1-y_obj2)**2)
    #accel = F/m = G*m_2/Distance**2 vers m2. 
    #TODO : 1-Trouver l'intensité de l'accélération 2-Faire x vecteur direction.
    #Vecteur unité : 
    vecteur_unite = [elem - object_relation.position[i] for i,elem in enumerate(obj.position)]
    magneture_unit_vector = math.sqrt(sum(i**2 for i in vecteur_unite))
    vecteur_unite = [-i/magneture_unit_vector for i in vecteur_unite]

    distance = magneture_unit_vector
    accel = G * object_relation.weight / distance**2
    #if obj.name=="Terre": print(accel)
    obj.accel = [obj.accel[index]+element * accel for index,element in enumerate(vecteur_unite)]




def update_vitesse(obj,dt):
    correction = 1
    obj.velocity = [elem+obj.accel[index]*dt*correction for index,elem in enumerate(obj.velocity)]

def update_positions(obj,dt):
    correction = 1
    obj.position = [elem+obj.velocity[index]*dt*correction for index,elem in enumerate(obj.position)]
    
def update_physics(objects, dt):

    for obj in objects:
        if obj.name!=obj.relation:
            if obj.name=="Terre": print(obj.velocity)
            update_accel(obj,objects,dt)
            update_vitesse(obj,dt)
            update_positions(obj,dt)
        
