from pyglet import shapes
import pyglet
from pyglet.gl import *
import math
#from states import SimulationState
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
#from src.engine import render
from celestial_objects import CelestialObject,create_celestial_objects,CELESTIAL_PARAMETERS,SimulationScale
from src.ui.pyglet_objects import Label,Button
import numpy as np
import ctypes


class OutilCreation:
    def __init__(self,textures,SimulationState,RenderTool):
        #Outil et autres init
        self.textures = textures
        self.RenderTool = RenderTool
        self.SimulationState = SimulationState
        self.object_created = Object_creation(None,None,None,None)
        self.angle_rotation = 0
        self.Titre_label = ""

        #États
        self.etats = ["texture","masse","rayon","position","choix_vitesse"]
        self.liste_etats = {"texture" : self.choix_texture, "masse" : self.choix_masse, "rayon": self.choix_rayon, "position":self.choix_position, "append_to_list":self.append_to_list,"choix_vitesse":self.choix_vitesse}
        self.etat_present = 0

        #crée la liste d'objets
        self.objects_creations = self.createObjectCreation()

        #Propriete:
        self.texture = None
        self.masse = 0
        self.rayon = 0
        self.position = [0,0,0]
        self.vitesse = [0,0,0]
        self.rec_opacity = 20
        self.rec2_opacity = 100

        #highlight Object Selection tecture
        self.selected_object_creation = None
        self.highlight_color = (0,1,1,0.3)
        self.label_sous_titre = ""
        self.type_object_celeste_mapping_color = {1:(250,237,97,200),2:(0,255,0,120),3:(139,69,19,150),4:(50,50,50,255)}
        self. label_sous_titre_color = (255,255,255,255)

        #Choix de position
        self.etat_present_SUB = 0

        #Choix vitesse
        self.G = 6.67430e-11
        self.choix_vitesse_object_centre = None
        self.choix_vitesse_force_initiale = 0

        #Souris
        self.souris_x = 0
        self.souris_y = 0

        self.appended = False

        #Sons
        self.confirmation_sound = pyglet.media.load('assets/sounds/confirm_creation.wav', streaming=False)


        self.CreationConfirmed = False



    def createObjectCreation(self):
        i = 1
        color = (25,25,25)
        liste = []
        for name, texture in self.textures.items():
            if name == "Soleil":
                object_type = 1
            elif name == "Black Hole":
                object_type = 4
            else:
                object_type = 2
            liste.append(Object_creation(name,texture,[i*color[n] for n,u in enumerate(color)],object_type))
            i+=1
        return liste
    def reset(self):
        self.highlight_color = (0,1,1,0.3)
        self.selected_object_creation = None
        self.etat_present = 0
        self.etat_present_SUB = 0
        self.object_created = Object_creation(None,None,None,None)

        if self.appended and not self.CreationConfirmed: #On enleve l'object si la creation n'a pas été confirmé
            self.SimulationState.objects.pop()
        self.appended = False
        self.CreationConfirmed = False
        self.choix_vitesse_object_centre = None
        self.choix_vitesse_force_initiale = 0


        

    def end(self):
        self.SimulationState.isCreating = False
        self.SimulationState.button_activation(True)
        self.SimulationState.pause()
        self.SimulationState.reset_positions()
        self.SimulationState.buttons[6].isOn = 1
        self.reset()

        
        

    def choix_texture(self): #ETAT #0 (PREMIER)
        self.Titre_label = "Select Celestial Object"
        self.dessiner_planets()


    def choix_masse(self): #ETAT #1 
        self.Titre_label = "Mass Specification"

    def choix_rayon(self):#ETAT #2 
        pass

    def choix_position(self):#ETAT #3 
        self.Titre_label = "Choose position"
        if 0.495 < self.souris_y < 0.505 :
            self.souris_y = 0.5

        if self.etat_present_SUB == 0:
            self.label_sous_titre = "Selection de l'axe des X"
            self.SimulationState.objects[-1].position_simulation[0] = (self.souris_x-0.5) * self.RenderTool.maxlength / 0.5
        elif self.etat_present_SUB == 1:
            self.SimulationState.objects[-1].position_simulation[2] = -(self.souris_y-0.5) * self.RenderTool.maxlength / 0.5
            self.label_sous_titre = "Selection de l'axe des Z"
        elif self.etat_present_SUB == 2:
            self.SimulationState.objects[-1].position_simulation[1] = (self.souris_y-0.5) * self.RenderTool.maxlength / 0.5
            self.label_sous_titre = "Selection de l'axe des Y"
        elif self.etat_present_SUB == 3:
            self.SimulationState.objects[-1].real_position = [SimulationScale.from_distance(coord) for coord in self.SimulationState.objects[-1].position_simulation]
            self.SimulationState.focus_on_axes("y")
            self.next_etat()




    def choix_vitesse(self):#ETAT #4 
        #Titre
        self.Titre_label = "Choose speed"

        #Étape 0 : Selection de l'object qui exerce la plus grande force, ajout de l'object dans self.choix_vitesse_object_centre
        #Etape 1 : Avec la souris, on calcul la vitesse initiale, puis on utilise cette vitesse pour dessiner l'éclipse
        #Etape 2 : Confirmation de la commande + Creation de l'object self.end()


        if self.etat_present_SUB == 0: #Etape 0
            self.choix_vitesse_object_centre, self.choix_vitesse_force_initiale = self.calcul_choix_vitesse_force()
            print("Here")
            self.etat_present_SUB+=1 
            self.SimulationState.focus_on_axes("y")

        elif self.etat_present_SUB == 1: #On determine la vitesse en X
            self.vitesse_Z = (self.souris_y-0.5) * 620 / 0.5
            self.label_sous_titre = f"{self.vitesse_Z:.1f} km/s" 
            self.draw_vecteur_vitesse()

    def draw_vecteur_vitesse(self):
        glPushMatrix()
        glColor3f(1, 1, 1)
        quadric = gluNewQuadric()
        gluSphere(quadric, 20, 100, 30)
        glPopMatrix()





    def append_to_list(self):#On ajoute l'object créé
        weight = 5.972e24
        color_id = [i+25 for i in self.SimulationState.objects[-1].color_id] 
        self.SimulationState.objects.append(CelestialObject(self.object_created.name,self.object_created.texture, texture_isLoaded=True,rayon_simulation=5,type_object=self.object_created.type_object,weight=2*weight,color_id=color_id))
        self.appended = True
    



    def draw_background(self): #Boucle pour Background

        self.padding = 5
        rec  = shapes.Rectangle(self.x, self.y, self.largeur, self.hauteur, color=(255,255,255))
        rec2 = shapes.Rectangle(self.x+self.padding,self.y+self.padding,self.largeur-2*self.padding, self.hauteur-2*self.padding, color=(1,1,1))
        rec.opacity = self.rec_opacity
        rec2.opacity = self.rec2_opacity
        rec.draw()
        rec2.draw()
        Label(self.RenderTool.window.get_size(), self.Titre_label, ((self.x+self.largeur)/2)/self.RenderTool.window.width, (self.y+self.hauteur)/self.RenderTool.window.height-0.06, self.SimulationState.font, (255, 255, 255, 200), 1.8).draw()
        Label(self.RenderTool.window.get_size(), self.label_sous_titre, ((self.x+self.largeur)/2)/self.RenderTool.window.width, (self.y+self.hauteur)/self.RenderTool.window.height-0.13, self.SimulationState.font, self.label_sous_titre_color, 2).draw()
    
    def draw(self):
        self.width = self.SimulationState.window.width
        self.height = self.SimulationState.window.height
        self.x = int(0.01 * self.width)
        self.y = int(0.38 * self.height)
        self.largeur = int(0.20*self.width)
        self.hauteur = int(0.5*self.height)

        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.draw_background()
        self.liste_etats[self.etats[self.etat_present]]()



    def next_etat(self):
        self.etat_present_SUB = 0
        if self.etat_present == 0:
            self.label_sous_titre =""
            self.etat_present = 3
            return

        self.etat_present += 1
    




    def contains_point(self, x, y): #Souris est sur le HUD
        return (self.x < x < self.x + self.largeur and
                self.y < y < self.y + self.hauteur)

    
    def on_mouse_motion(self,x,y):
        if self.contains_point(x,y):
            if self.etat_present == 0:
                self.selected_object_creation = self.RenderTool.selection_mode(x,y,mode=1,liste_objects = self.objects_creations)
                if self.selected_object_creation:
                    self.label_sous_titre_color = self.type_object_celeste_mapping_color.get(self.selected_object_creation.type_object)
                    self.label_sous_titre = self.selected_object_creation.name
                else:
                    self.label_sous_titre = ""
        if self.etat_present == 3 or self.etat_present == 4:
            self.souris_x = x/self.width
            self.souris_y = y/self.height


    def axe_rotation_position(self):
        if self.etat_present_SUB == 0:
            self.SimulationState.focus_on_axes("y")
        elif self.etat_present_SUB ==1 :
            self.SimulationState.focus_on_axes("y")
        elif self.etat_present_SUB == 2 :
            self.SimulationState.focus_on_axes("z")

    def calculate_mouse_distance(self):
        # Ajustez les coordonnées de la souris pour qu'elles soient centrées autour de (0.5, 0.5)
        centered_x = self.souris_x - 0.5
        centered_y = self.souris_y - 0.5
        
        # Calculez la distance par rapport au centre
        distance = (centered_x**2 + centered_y**2)**0.5
        
        return distance


    def on_mouse_drag(self,x,y):
        pass

    def on_mouse_press(self,x,y):
        self.highlight_color=(1,1,1,0.2)




    def on_mouse_release(self,x,y):
        if self.etat_present == 0: #CHOIX DES TEXTURES
            self.selected_object_creation = self.RenderTool.selection_mode(x,y,mode=1,liste_objects = self.objects_creations)
            if self.selected_object_creation:
                self.object_created.texture = self.selected_object_creation.texture
                self.object_created.name = self.selected_object_creation.name
                self.highlight_color = (0,1,1,0.3)
                self.append_to_list()
                self.next_etat()
                self.RenderTool.axesEnable = True
                self.SimulationState.focus_on_axes("y")


    def on_key_press(self,symbol):
        if symbol == pyglet.window.key.Q:
            if self.etat_present == 3: #CHOIX DES POSITIONS
                self.etat_present_SUB+=1
                self.axe_rotation_position()

    
        if symbol == pyglet.window.key.E:
            if self.etat_present == 3: #Si en mode position
                if self.etat_present_SUB > 0: #On change entre les axes
                    self.etat_present_SUB-=1
                    self.axe_rotation_position()
                else: #Si en premier axe(X), on passe à l'état précedant
                    self.reset()
                    self.etat_present = 0
        if symbol == pyglet.window.key.ESCAPE:
            self.end()




    def calcul_choix_vitesse_force(self):
        object_orbite = self.SimulationState.objects[-1]
        max_force = 0
        max_object = None
        for obj in self.SimulationState.objects[:-1]:
            force = self.calcul_force(obj.weight,object_orbite.weight,obj.real_position,object_orbite.real_position)
            if force > max_force:
                max_force = force
                max_object = obj
        return max_object,max_force

    def calcul_force(self,m1,m2,p1,p2):
        distance = np.linalg.norm(np.array(p1) - np.array(p2))
        force = (self.G*m1*m2)/(distance**2)
        #print(f"Distance : {distance}        force : {force}")
        return force




    def dessiner_planets(self):
        self.angle_rotation += 1

        glViewport(self.x + self.padding, self.y + self.padding, self.largeur - 2 * self.padding, self.hauteur - 2 * self.padding)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        fov = 35
        aspect_ratio = (self.largeur - 2 * self.padding) / (self.hauteur - 2 * self.padding)
        near = 0.1
        far = 100
        gluPerspective(fov, aspect_ratio, near, far)

        glEnable(GL_TEXTURE_2D)

        num_planets_per_row = 3
        planet_radius = 3.5
        gap = 2.3 * planet_radius
        titre_marge = 1 * planet_radius  # Adjust as needed

        half_width_of_line = 2 * gap + num_planets_per_row * 2 * planet_radius + (num_planets_per_row - 1) * gap
        half_height_of_line = 2 * planet_radius

        start_x = -0.9*half_width_of_line / 2 + gap
        start_y = half_height_of_line / 2 + titre_marge

        row_count = 0
        col_count = 0
        labels = []

        for obj in self.objects_creations:
            glPushMatrix()
            #draw planets
            # Translation to position the planet
            glTranslatef(start_x + col_count * (gap + 2 * planet_radius), start_y - row_count * (gap + 2 * planet_radius), -100)
            glRotatef(self.angle_rotation, 0, 1, 1)

            glBindTexture(GL_TEXTURE_2D, obj.texture.id)

            quadric = gluNewQuadric()
            gluQuadricTexture(quadric, GL_TRUE)
            gluSphere(quadric, planet_radius, 100, 30)

            #Draw selection
            if self.selected_object_creation and obj == self.selected_object_creation:
                glDisable(GL_TEXTURE_2D)
                glEnable(GL_BLEND)
                glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
                glDisable(GL_DEPTH_TEST)

                quadric = gluNewQuadric()
                glColor4f(*self.highlight_color)
                color = self.type_object_celeste_mapping_color.get(self.selected_object_creation.type_object)[:3]
                color = [n/255 for n in color]
                for i in range(1,30):
                    glColor4f(*color,0.15/i)
                    gluSphere(quadric,planet_radius*(1+0.04*i),100,30)
                glDisable(GL_BLEND)
                glEnable(GL_TEXTURE_2D)
                glColor4f(1,1,1,1)
            glPopMatrix()

            col_count += 1
            if col_count == num_planets_per_row:
                col_count = 0
                row_count += 1

        glDisable(GL_TEXTURE_2D)

        # Restore the previous projection
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glViewport(0, 0, self.width, self.height)





class Object_creation:
    def __init__(self,name,texture,color_id,type_object):
        self.name = name
        self.texture = texture
        self.color_id = color_id
        self.type_object = type_object