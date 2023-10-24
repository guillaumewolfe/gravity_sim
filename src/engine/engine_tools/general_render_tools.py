from pyglet.gl import *
from pyglet.text import Label
import math
from engine_tools.FrameBuffer import FrameBuffer
from engine_tools.minimap import Minimap
from ctypes import c_char_p,POINTER,c_int,cast
from pyglet import shapes
import ctypes
import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.ui.pyglet_objects import Label,Button
from src.ui.states import SimulationState


class GeneralRenderTools:
    def __init__(self,RenderScript):
        self.rd = RenderScript




    def draw_planet_path(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LINE_SMOOTH)
        glDisable(GL_DEPTH_TEST)
        #glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

        for obj in self.rd.objects:
            if obj.drawOrbitEnable and len(obj.position_history) > 2 and obj.name != "Lune":
                glLineWidth(2)
                glBegin(GL_LINE_STRIP)
                path_length = len(obj.position_history)  # Define the path_length here
                for index, position in enumerate(obj.position_history):
                    alpha = 0.60*(index / (path_length - 1))
                    glColor4f(1, 1, 1, alpha)
                    glVertex3f(position[0], position[1], position[2])
                glEnd()  # Ensure glEnd is called for each object's path

        glColor4f(1, 1, 1, 1)  # Reset color
        glLineWidth(1)    
        glEnable(GL_DEPTH_TEST)
        


    def draw_axes(self, length=50, position = [0,0,0]):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
        nbre_line = 20
        glBegin(GL_LINES)
        length = self.rd.maxlength

        glColor4f(1,1,1,0.5)
        #Axe X
        glVertex3f(position[0],position[1],position[2])
        glVertex3f(position[0]+length,position[1],position[2])
        
        #Axe Z
        glVertex3f(position[0],position[1],position[2])
        glVertex3f(position[0],position[1],position[2]+length)
        
        #Axe Y
        glVertex3f(position[0],position[1],position[2])
        glVertex3f(position[0],position[1]+length,position[2])
        # Drawing the grid with 50% opacity

        grid_spacing = length/nbre_line
        glColor4f(1,1,1,0.2)

        temps = 10
        if not self.rd.axesDrawned:
            dynamic_offset_factor = self.rd.frame_counter_axes/temps
            self.rd.frame_counter_axes+=1
            if self.rd.frame_counter_axes >= temps:
                self.rd.axesDrawned = True
        else:
            dynamic_offset_factor = 1



        for i in range(0, nbre_line):
            offset = i * grid_spacing
            dynamic_offset = offset*dynamic_offset_factor
            
            # Grid lines parallel to X-axis (both positive and negative Z direction)
            glVertex3f(position[0] - length, position[1], position[2] + dynamic_offset)
            glVertex3f(position[0] + length, position[1], position[2] + dynamic_offset)
            
            glVertex3f(position[0] - length, position[1], position[2] - dynamic_offset)
            glVertex3f(position[0] + length, position[1], position[2] - dynamic_offset)

            # Grid lines parallel to Z-axis (both positive and negative X direction)
            glVertex3f(position[0] + dynamic_offset, position[1], position[2] - length)
            glVertex3f(position[0] + dynamic_offset, position[1], position[2] + length)
            
            glVertex3f(position[0] - dynamic_offset, position[1], position[2] - length)
            glVertex3f(position[0] - dynamic_offset, position[1], position[2] + length)


        glColor4f(1,1,1,1)
        glEnd()
        glDisable(GL_BLEND)



    def draw_highlight(self, obj):
        scale_factor = 0.5 * math.sin(2 * math.pi * self.rd.frame_counter / 90) + 0.5  # This oscillates between 0 and 1 over 60 frames
        position = obj.position_simulation
        """Draw a semi-transparent sphere around the selected object."""
        # Color (47,233,240) with 0.5 transparency
        colors = (255,255,255)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)

        glColor4f(colors[0]/255, colors[1]/255, colors[2]/255, 0.10)
        

        glPushMatrix()
        
        # Translate to the object's position
        glTranslatef(position[0], position[1], position[2])
        
        # Scale if necessary. You can adjust or remove this line depending on your needs.
        #glScalef(scale, scale, scale)
        
        # Drawing the sphere (assuming you have the glu library with pyglet)
        quad = gluNewQuadric()
        for i in range(1,25):
            glColor4f(1.0,1.0,1,(0.04+scale_factor/20)/(i))
            gluSphere(quad,obj.rayon_simulation*(1+0.015*i),100,100)
        gluDeleteQuadric(quad)


        glPopMatrix()
        glColor4f(1, 1, 1, 1)



    def follow_line(self,position):
        glBegin(GL_LINES)
        glColor4f(1,1,1,0.6)
        #Lign from the sun to the object
        if self.rd.followLineEnable:
            glVertex3f(0,0,0)
            glVertex3f(position[0],position[1],position[2])
        glColor4f(1,1,1,1)
        glEnd()







    def draw_selected_object_infos(self, object):
        y = 0.42
        x = 0.82
        largeur = 0.16
        hauteur = 0.53
        padding = 4
        rec = shapes.Rectangle(self.rd.window.width * x, self.rd.window.height * y, self.rd.window.width * largeur, self.rd.window.height * hauteur, color=(41, 50, 69)) 
        rec2 = shapes.Rectangle(self.rd.window.width * x - padding / 2, self.rd.window.height * y - padding / 2, self.rd.window.width * largeur + padding, self.rd.window.height * hauteur + padding, color=(255, 255, 255)) 
        rec.opacity = 120 
        rec2.opacity = 20
        # Dessinez l'écriture
        centrer_x = (self.rd.window.width * (x + largeur / 2))/self.rd.window.width
        centrer_y = (self.rd.window.height * (y + hauteur - 0.035))/self.rd.window.height
        # Configurez le viewport pour les rectangles
    

        # Dessinez les rectangles directement sans aucune modification de la projection
        rec2.draw()
        rec.draw()
        diff = 0.025
        hauteur_vitesse = 0.12
        type_object = self.rd.type_object_celeste_mapping.get(object.type_object)
        couleur_type_object = self.rd.type_object_celeste_mapping_color.get(object.type_object)
        Label(self.rd.window.get_size(), f'{object.name}', centrer_x, centrer_y, self.rd.font, (255, 255, 255, 200), 2.5).draw()
        Label(self.rd.window.get_size(), f'{type_object}', centrer_x, centrer_y-0.035, self.rd.font, couleur_type_object, 1.5).draw()
        Label(self.rd.window.get_size(), "Vitesse", centrer_x, centrer_y-0.10, self.rd.font, (255,255,255,200), 1.5).draw()
        Label(self.rd.window.get_size(), f"{object.get_velocity():,.0f} km/h".replace(",", ' '), centrer_x, centrer_y-0.125, self.rd.font, (255,255,255,150), 1.2).draw()

        Label(self.rd.window.get_size(), "Masse", centrer_x, centrer_y-0.160, self.rd.font, (255,255,255,200), 1.5).draw()
        Label(self.rd.window.get_size(), f"{object.weight:,.2e} kg".replace(",", ' '), centrer_x, centrer_y-0.160-diff, self.rd.font, (255,255,255,150), 1.2).draw()

        Label(self.rd.window.get_size(), "Rayon", centrer_x, centrer_y-0.155-diff-0.05, self.rd.font, (255,255,255,200), 1.5).draw()
        Label(self.rd.window.get_size(), f"{object.real_radius/1000:,.0f} km".replace(",", ' '), centrer_x, centrer_y-0.155-2*diff-0.05, self.rd.font, (255,255,255,150), 1.2).draw()

        if object.type_object !=1:
            Label(self.rd.window.get_size(), "Force gravitationnelle", centrer_x, centrer_y-0.155-2*diff-2*0.05, self.rd.font, (255,255,255,200), 1.5).draw()
            Label(self.rd.window.get_size(), f"{object.get_force():,.2e} N".replace(",", ' '), centrer_x, centrer_y-0.155-3*diff-2*0.05, self.rd.font, (255,255,255,150), 1.2).draw()
        else:
            Label(self.rd.window.get_size(), "Température", centrer_x, centrer_y-0.155-2*diff-2*0.05, self.rd.font, (255,255,255,200), 1.5).draw()
            Label(self.rd.window.get_size(), f"5 500 k".replace(",", ' '), centrer_x, centrer_y-0.155-3*diff-2*0.05, self.rd.font, (255,255,255,150), 1.2).draw()


        glViewport(int(self.rd.window.width * x), int(self.rd.window.height * y), int(self.rd.window.width * largeur), int(self.rd.window.height * hauteur))
        # Configurez la projection pour le rendu 3D
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        fov = 35
        aspect_ratio = (self.rd.window.width * largeur) / (self.rd.window.height * hauteur)
        near = 0.1
        far = 100
        gluPerspective(fov, aspect_ratio, near, far)

        # Dessinez la sphère
        glEnable(GL_TEXTURE_2D)
        glPushMatrix()
        # Placez la caméra un peu plus loin pour voir correctement la sphère
        glTranslatef(0, -19.5, -100)
        #glRotatef(90,1,0,0)
        self.rd.rotation_matrix = self.rd.extract_rotation_matrix(self.rd.matrix)
        glMultMatrixd(self.rd.rotation_matrix)
        glBindTexture(GL_TEXTURE_2D, object.texture.id)
        glRotatef(self.rd.selectedObject.rotation_siderale_angle,*self.rd.selectedObject.rotation_direction)
        quadric = gluNewQuadric()
        gluQuadricTexture(quadric, GL_TRUE)
        #object.rayon_simulation
        gluSphere(quadric, 4, 100, 30)
        glPopMatrix()

        glDisable(GL_TEXTURE_2D)

        # Restaurez la projection précédente
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        # Réinitialisez le viewport à ses dimensions originales
        glViewport(0, 0, self.rd.window.width, self.rd.window.height)


    

    def draw_quad_with_offset(self, offset_x, offset_y, zoom_factor=1.0):
        # Calculate the zoomed dimensions
        zoomed_width = self.rd.window.width * zoom_factor
        zoomed_height = self.rd.window.height * zoom_factor

        # Calculate the difference to adjust the vertices
        diff_width = (self.rd.window.width - zoomed_width) / 2
        diff_height = (self.rd.window.height - zoomed_height) / 2

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(diff_width + offset_x, diff_height + offset_y)
        glTexCoord2f(1, 0)
        glVertex2f(zoomed_width + offset_x, diff_height + offset_y)
        glTexCoord2f(1, 1)
        glVertex2f(zoomed_width + offset_x, zoomed_height + offset_y)
        glTexCoord2f(0, 1)
        glVertex2f(diff_width + offset_x, zoomed_height + offset_y)
        glEnd()

    def set_background(self):
        glEnable(GL_TEXTURE_2D)

        rotation_offset_x = self.rd.rotation_y*0.01
        rotation_offset_y = -self.rd.rotation_x*0.01



        offset_x1 = self.rd.translation_x * 0.01 + rotation_offset_x
        offset_y1 = self.rd.translation_y * 0.01 + rotation_offset_y

        glBindTexture(GL_TEXTURE_2D, self.rd.bg_texture2.id)
        self.draw_quad_with_offset(offset_x1,offset_y1)

        offset_x2 = self.rd.translation_x * 0.05 + rotation_offset_x
        offset_y2 = self.rd.translation_y * 0.05 + rotation_offset_y
        
        glBindTexture(GL_TEXTURE_2D, self.rd.bg_texture2.id)
        self.draw_quad_with_offset(offset_x2,offset_y2,2)


        offset_x3 = self.rd.translation_x * 2 - rotation_offset_x*20
        offset_y3 = self.rd.translation_y * 2 - rotation_offset_y*20

        glBindTexture(GL_TEXTURE_2D, self.rd.background_texture.id)
        self.draw_quad_with_offset(offset_x3,offset_y3,2)

    




        glDisable(GL_TEXTURE_2D)

