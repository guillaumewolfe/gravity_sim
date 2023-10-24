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
    def __init__(self,objects,SimulationState,RenderTool):
        #Outil et autres init
        self.RenderTool = RenderTool
        self.SimulationState = SimulationState
        self.object_created = CelestialObject(None,None)
        self.angle_rotation = 0
        self.Titre_label = ""

        #États
        self.etats = ["texture","masse","rayon","position","choix_vitesse"]
        self.liste_etats = {"texture" : self.choix_texture, "masse" : self.choix_masse, "rayon": self.choix_rayon, "position":self.choix_position, "append_to_list":self.append_to_list,"choix_vitesse":self.choix_vitesse}
        self.etat_present = 0
        self.etat_present_SUB = 0

        #crée la liste d'objets
        self.objects_creations = self.select_object(objects)
        self.buttons = []

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


        self.x = 0
        self.y = 0
        self.largeur = 0
        self.hauteur = 0

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


    def select_object(self,objects):
        liste = []
        for obj in objects:
            if obj.name != "Lune" and obj.name != "Saturne" and obj.name != "Mercure":
                liste.append(obj)
        return liste
    

    def reset(self):
        self.highlight_color = (0,1,1,0.3)
        self.selected_object_creation = None
        self.etat_present = 0
        self.etat_present_SUB = 0
        self.object_created = CelestialObject(None,None)
        self.buttons = []

        if self.appended and not self.CreationConfirmed: #On enleve l'object si la creation n'a pas été confirmé
            self.SimulationState.objects.pop()
        self.appended = False
        self.CreationConfirmed = False
        self.choix_vitesse_object_centre = None
        self.choix_vitesse_force_initiale = 0
        self.label_sous_titre=""


        

    def end(self):
        self.SimulationState.isCreating = False
        self.SimulationState.button_activation(True)
        self.SimulationState.pause()
        self.SimulationState.reset_positions()
        self.SimulationState.buttons[6].isOn = 1
        self.reset()
        self.RenderTool.axesEnable = False

        
        

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
            self.label_sous_titre = "Distance du soleil"
            self.SimulationState.objects[-1].position_simulation[0] = (self.souris_x-0.5) * self.RenderTool.maxlength*0.1*(1-0.1*(self.RenderTool.zoom+500)/500)
            self.SimulationState.objects[-1].position_simulation[2] = -(self.souris_y-0.5) * self.RenderTool.maxlength *0.1*(1-0.1*(self.RenderTool.zoom+500)/500)
            Label(self.RenderTool.window.get_size(), f"{self.calcul_real_distance(self.SimulationState.objects[-1])/(1000*1.496e8):.2f} UA", ((self.x+self.largeur)/2)/self.RenderTool.window.width, (self.y+self.hauteur)/self.RenderTool.window.height-0.25, self.SimulationState.font, (255, 255, 255, 200), 3).draw()
            Label(self.RenderTool.window.get_size(), f"{self.calcul_real_distance(self.SimulationState.objects[-1])/(1000):,.0f} km".replace(",", ' '), ((self.x+self.largeur)/2)/self.RenderTool.window.width, (self.y+self.hauteur)/self.RenderTool.window.height-0.30, self.SimulationState.font, (255, 255, 255, 200), 1.3).draw()            
            #print(f"{self.calcul_real_distance(self.SimulationState.objects[-1])/1000:.0f} km")
        elif self.etat_present_SUB == 1:
            self.SimulationState.objects[-1].position_simulation[1] = (self.souris_y-0.5) * self.RenderTool.maxlength*0.1
            self.label_sous_titre = "Selection de la hauteur"
            Label(self.RenderTool.window.get_size(), f"{self.calcul_real_distance(self.SimulationState.objects[-1])/(1000*1.496e8):.2f} UA", ((self.x+self.largeur)/2)/self.RenderTool.window.width, (self.y+self.hauteur)/self.RenderTool.window.height-0.25, self.SimulationState.font, (255, 255, 255, 200), 3).draw()
            Label(self.RenderTool.window.get_size(), f"{self.calcul_real_distance(self.SimulationState.objects[-1])/(1000):,.0f} km".replace(",", ' '), ((self.x+self.largeur)/2)/self.RenderTool.window.width, (self.y+self.hauteur)/self.RenderTool.window.height-0.30, self.SimulationState.font, (255, 255, 255, 200), 1.3).draw()
        elif self.etat_present_SUB == 2: #Fin
            self.SimulationState.objects[-1].real_position = [SimulationScale.from_distance(coord) for coord in self.SimulationState.objects[-1].position_simulation]
            self.next_etat()




    def choix_vitesse(self):#ETAT #4 
        #Titre
        #Étape 0 : Selection de l'object qui exerce la plus grande force, ajout de l'object dans self.choix_vitesse_object_centre
        #Etape 1 : Avec la souris, on calcul la vitesse initiale, puis on utilise cette vitesse pour dessiner l'éclipse
        #Etape 2 : Confirmation de la commande + Creation de l'object self.end()


        if self.etat_present_SUB == 0: #Etape 0
            self.Titre_label = "Choose speed"
            self.label_sous_titre=""
            self.buttons.append(Button(self.RenderTool.window, 0.25*(((self.x+self.largeur)/2)/self.RenderTool.window.width), (self.y+self.hauteur)/self.RenderTool.window.height-0.20,0.015, 0.035,"-",(255,255,255),self.SimulationState.font,opacity=50,isHighlight=True,highlight_color=(255,0,0,35),id="-vitesse"))
            self.buttons.append(Button(self.RenderTool.window, 1.85*(((self.x+self.largeur)/2)/self.RenderTool.window.width), (self.y+self.hauteur)/self.RenderTool.window.height-0.20,0.015, 0.035,"+",(255,255,255),self.SimulationState.font,opacity=50,isHighlight=True,highlight_color=(0,255,0,35),id="+vitesse"))
            self.buttons.append(Button(self.RenderTool.window, (((self.x+self.largeur)/2)/self.RenderTool.window.width), (self.y)/self.RenderTool.window.height+0.025,0.07, 0.035,"Confirm",(255,255,255),self.SimulationState.font,opacity=20,isHighlight=True,highlight_color=(0,255,0,80)))
            self.choix_vitesse_object_centre, self.choix_vitesse_force_initiale = self.calcul_choix_vitesse_force()
            self.axe_rotation_position()
            self.etat_present_SUB+=1 
            self.vitesse_dic,self.vitesse_list = self.calculate_predefined_velocity(self.SimulationState.objects[-1],self.choix_vitesse_object_centre)
            self.index_vitesse_list = 0

        elif self.etat_present_SUB == 1: #On determine la vitesse en X
            current_speed_label = self.vitesse_list[self.index_vitesse_list]
            self.current_speed_value = self.vitesse_dic[current_speed_label]
            Label(self.RenderTool.window.get_size(), current_speed_label, ((self.x+self.largeur)/2)/self.RenderTool.window.width, (self.y+self.hauteur)/self.RenderTool.window.height-0.18, self.SimulationState.font, (255, 255, 255, 200), 1.5).draw()
            Label(self.RenderTool.window.get_size(), f"{self.current_speed_value:.0f} km/h", ((self.x+self.largeur)/2)/self.RenderTool.window.width, (self.y+self.hauteur)/self.RenderTool.window.height-0.21, self.SimulationState.font, (255, 255, 255, 200), 1.5).draw()
            
        elif self.etat_present_SUB == 2:
            self.SimulationState.objects[-1].velocity = self.compute_speed_vector(self.current_speed_value,self.SimulationState.objects[-1],self.choix_vitesse_object_centre)
            self.CreationConfirmed = True
            self.end()




    def append_to_list(self):#On ajoute l'object créé
        color_id = [i+25 for i in self.SimulationState.objects[-1].color_id] 
        self.SimulationState.objects.append(CelestialObject("Creation",self.object_created.texture, texture_isLoaded=True,rayon_simulation=self.object_created.rayon_simulation,type_object=self.object_created.type_object,weight=self.object_created.weight,color_id=color_id,isCreated = True))
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
        Label(self.RenderTool.window.get_size(), self.label_sous_titre, ((self.x+self.largeur)/2)/self.RenderTool.window.width, (self.y+self.hauteur)/self.RenderTool.window.height-0.11, self.SimulationState.font, self.label_sous_titre_color, 2).draw()
    
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

        if self.buttons:
            for btn in self.buttons:
                btn.draw()



    def next_etat(self,valeur=1):
        self.etat_present_SUB = 0
        if self.etat_present == 0:
            self.label_sous_titre =""
            self.etat_present = 3
            return

        self.etat_present += valeur
        self.buttons=[]
    




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
        if self.buttons:
            for btn in self.buttons:
                if btn.contains_point(x, y):
                    btn.hover = True
                else:
                    btn.hover = False

    def on_mouse_click(self,x,y):
        if self.buttons:
            for btn in self.buttons:
                btn.click()


    def axe_rotation_position(self):
        zoom_out = 200
        if self.etat_present_SUB == 0:
            self.SimulationState.focus_on_axes("y",reset=False)
        elif self.etat_present_SUB == 1 :
            self.SimulationState.focus_on_axes("z",reset=False)
        self.SimulationState.zoomer(-zoom_out)


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
        print("here")
        self.highlight_color=(1,1,1,0.2)



    def on_mouse_release(self,x,y):
        if self.buttons:
            for btn in self.buttons:
                btn.unclick()
            self.button_pressed(x,y)
        if self.etat_present == 0: #CHOIX DES TEXTURES
            self.selected_object_creation = self.RenderTool.selection_mode(x,y,mode=1,liste_objects = self.objects_creations)
            if self.selected_object_creation:
                self.object_created= self.selected_object_creation
                self.highlight_color = (0,1,1,0.3)
                self.append_to_list()
                self.next_etat()
                self.RenderTool.axesEnable = True
                self.axe_rotation_position()


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
                    self.next_etat(-1)
        if symbol == pyglet.window.key.ESCAPE:
            self.end()


    def button_pressed(self,x,y):
        for btn in self.buttons:
            if btn.contains_point(x, y):
                if btn.id == "+vitesse":
                    if self.index_vitesse_list< len(self.vitesse_list) - 1:
                        self.index_vitesse_list += 1
                if btn.id == "-vitesse":
                    if self.index_vitesse_list>0:
                        self.index_vitesse_list-=1
                if btn.id == "Confirm":
                    self.etat_present_SUB += 1

    def calculate_predefined_velocity(self,obj_in_orbit,obj_in_middle):
        vitesse_dic = {"":0}
        #Orbital speed
        orbit_speed = ((self.G*obj_in_middle.weight)/self.calcul_real_distance(obj_in_orbit))**0.5
        vitesse_dic["Circular orbit"]=orbit_speed
        #Escape Velocity
        escape_velocity_speed = ((2*self.G*obj_in_middle.weight)/self.calcul_real_distance(obj_in_orbit))**0.5
        vitesse_dic["Escape Velocity"]=escape_velocity_speed

        vitesse_list = list(vitesse_dic.keys())
        return vitesse_dic,vitesse_list




    def calcul_real_distance(self,obj):
        real_position = [SimulationScale.from_distance(coord) for coord in obj.position_simulation]
        return (real_position[0]**2+real_position[1]**2+real_position[2]**2)**0.5

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


    def compute_speed_vector(self,vitesse,obj,obj_centre):
        if vitesse == 0:
            return [0,0,0]
        object_position = np.array([obj.real_position[0], obj.real_position[1], obj.real_position[2]])
        object_centre = np.array([obj_centre.real_position[0], obj_centre.real_position[1], obj_centre.real_position[2]])

        direction_vector = object_centre - object_position #vecteur direction entre obj et son object au centre
        direction_length = np.linalg.norm(direction_vector) #Norme du vecteur direction
        normalized_direction = direction_vector / direction_length #Vecteur direction normalisé

        vertical_vector = np.array([0, 1, 0])  # Vecteur vertical
        perpendicular_vector = np.cross(normalized_direction, vertical_vector)


        perpendicular_length = np.linalg.norm(perpendicular_vector)
        normalized_perpendicular = perpendicular_vector / perpendicular_length

        object_velocity = vitesse * normalized_perpendicular
        vx, vy, vz = object_velocity
        velocity_list = [vx, vy, vz]
        return velocity_list


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





