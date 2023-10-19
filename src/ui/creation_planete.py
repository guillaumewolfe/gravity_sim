from pyglet import shapes
from pyglet.gl import *
import math
#from states import SimulationState
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
#from src.engine import render
from celestial_objects import CelestialObject,create_celestial_objects,CELESTIAL_PARAMETERS
from src.ui.pyglet_objects import Label,Button


class OutilCreation:
    def __init__(self,textures,SimulationState,RenderTool):

        self.textures = textures
        self.RenderTool = RenderTool
        self.SimulationState = SimulationState

        self.object_created = None

        #États
        self.etats = ["texture","masse","rayon","position","choix_vitesse","append_to_list"]
        self.liste_etats = {"texture" : self.choix_texture, "masse" : self.choix_masse, "rayon": self.choix_rayon, "position":self.choix_position, "append_to_list":self.append_to_list,"vitesse":self.choix_vitesse}
        self.etat_present = 0

        #Propriete:
        self.texture = None
        self.masse = 0
        self.rayon = 0
        self.position = [0,0,0]
        self.vitesse = [0,0,0]
        self.rec_opacity = 100
        self.rec2_opacity = 200

        self.angle_rotation = 0

        

        #ViewPort

    def choix_texture(self):
        choix = False
        self.dessiner_planets()



        if choix:
            self.next_etat()
    def choix_masse(self):
        print("masse")

    def choix_rayon(self):
        pass

    def choix_position(self):
        pass

    def choix_vitesse(self):
        pass

    def append_to_list(self):
        pass




    def draw_background(self):

        self.padding = 5
        rec  = shapes.Rectangle(self.x, self.y, self.largeur, self.hauteur, color=(255,255,255))
        rec2 = shapes.Rectangle(self.x+self.padding,self.y+self.padding,self.largeur-2*self.padding, self.hauteur-2*self.padding, color=(1,1,1))
        rec.opacity = self.rec_opacity
        rec2.opacity = self.rec2_opacity
        rec.draw()
        rec2.draw()
        Label(self.RenderTool.window.get_size(), f'Type de planète', ((self.x+self.largeur)/2)/self.RenderTool.window.width, (self.y+self.hauteur)/self.RenderTool.window.height-0.04, self.SimulationState.font, (255, 255, 255, 200), 1.5).draw()


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
        self.etat_present += 1
    




    def contains_point(self, x, y):
        return (self.x < x < self.x + self.largeur and
                self.y < y < self.y + self.hauteur)

    
    def on_mouse_motion(self,x,y):
       pass



    def mouse_drag(self,x,y):
        pass


    def mouse_click(self,x,y):
        pass


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
        planet_radius = 3
        gap = 3 * planet_radius
        titre_marge = 2 * planet_radius  # Adjust as needed

        half_width_of_line = 2 * gap + num_planets_per_row * 2 * planet_radius + (num_planets_per_row - 1) * gap
        half_height_of_line = 2 * planet_radius

        start_x = -0.9*half_width_of_line / 2 + gap
        start_y = half_height_of_line / 2 + titre_marge

        row_count = 0
        col_count = 0
        labels = []

        for planet_name, texture in self.textures.items():
            glPushMatrix()

            # Translation to position the planet
            glTranslatef(start_x + col_count * (gap + 2 * planet_radius), start_y - row_count * (gap + 2 * planet_radius), -100)
            glRotatef(self.angle_rotation, 0, 1, 1)

            glBindTexture(GL_TEXTURE_2D, texture.id)

            quadric = gluNewQuadric()
            gluQuadricTexture(quadric, GL_TRUE)
            gluSphere(quadric, planet_radius, 100, 30)

            glPopMatrix()

            # Update counters to position the next planet
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
        row_count = 0
        col_count = 0
        labels = []
        """
        # Draw all the labels after restoring the projection
        for planet_name, texture in self.textures.items():

            x_label_relative_to_planet = start_x + col_count * (gap + 2 * planet_radius)
            y_label_relative_to_planet = start_y - row_count * (gap + 2 * planet_radius) - 2.5 * planet_radius


            x_label_window = (x_label_relative_to_planet / half_width_of_line + 1) * 0.5 * (self.largeur - 2 * self.padding) + self.x + self.padding
            y_label_window = (y_label_relative_to_planet / half_height_of_line + 1) * 0.5 * (self.hauteur - 2 * self.padding) + self.y + self.padding

            labels.append(Label(self.RenderTool.window.get_size(), f'{planet_name}', x_label_window / self.RenderTool.window.width, y_label_window / self.RenderTool.window.height, self.SimulationState.font, (255, 255, 255, 200), 3))



        for label in labels:
            label.draw()"""



"""        if self.SimulationState.isCreating:
            self.SimulationState.OutilCreation.draw()"""