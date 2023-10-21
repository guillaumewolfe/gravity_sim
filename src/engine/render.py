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

class RenderTool:
    def __init__(self,window, labels, buttons, objects, rotation_x, rotation_y, rotation_z, translation_x,translation_y,zoom,backgroundTexture,font=None,SimulationState = None):
        #Fenêtre
        self.window = window
        self.SimulationState = SimulationState
        #Objects
        self.objects = objects
        self.labels = labels
        self.buttons = buttons
        self.font = font

        #Camera settings
        self.rotation_x = rotation_x
        self.rotation_y = rotation_y
        self.rotation_z = rotation_z
        self.translation_x = translation_x
        self.translation_y = translation_y
        self.zoom = zoom

        self.translation_initiale = (0, 0,-150)
        self.rotation_initiale = (0,100, 10.5)

        #Initiate only
        self.background_texture = backgroundTexture
        self.frameBuffer = FrameBuffer(*window.get_size())

        #Selection
        self.selectedObject = None
        self.followObjectEnabled = False
        self.followObject = None

        #Highligh
        self.frame_counter = 0

        #Axe et plane
        self.axesEnable = False
        self.axesDrawned = False
        self.frame_counter_axes = 0
        self.planeEnable = True
        self.followLineEnable = True
        self.maxlength = 5

        #Infos planètes
        self.type_object_celeste_mapping = {1:"Étoile",2:"Planète",3:"Astéroide",4:"Trou Noir"}
        op = 150
        self.type_object_celeste_mapping_color = {1:(250,237,97,op),2:(0,255,0,op),3:(139,69,19,op),4:(1,1,1,op)}





        #Background
        self.bg_texture1 = pyglet.image.load('assets/textures/background_alpha1.png').get_texture()
        self.bg_texture2 = pyglet.image.load('assets/textures/background2.jpg').get_texture()
        self.bg_texture3 = pyglet.image.load('assets/textures/background3.jpg').get_texture()
        self.bg_texture4 = pyglet.image.load('assets/textures/background4.jpg').get_texture()
        self.saturn_ring = pyglet.image.load('assets/textures/saturn_ring2.png').get_texture()
    
    def update(self,labels, buttons, objects, rotation_x, rotation_y, rotation_z, translation_x,translation_y,zoom):
        #Update des objets et cameras settings selon le changement fait dans l'état
        #Objects
        self.objects = objects
        self.labels = labels
        self.buttons = buttons

        #Camera settings
        self.rotation_x = rotation_x
        self.rotation_y = rotation_y
        self.rotation_z = rotation_z
        self.translation_x = translation_x
        self.translation_y = translation_y
        self.zoom = zoom

    def draw_minimap(self):
        padding = 3
        rec  = shapes.Rectangle(0, 0, self.window.width*0.20, self.window.height*0.30, color=(1,1,1))
        rec2  = shapes.Rectangle(0, 0, self.window.width*0.20+2*padding, self.window.height*0.30+2*padding, color=(255,255,255))
        x_rel = 0.01
        y_rel = 0.02
        x = self.window.width * x_rel 
        y = self.window.height * y_rel 


        rec.x = x
        rec.y = y
        rec2.x = x - padding
        rec2.y = y - padding
        rec2.opacity = 20
        rec.opacity = 200
        rec2.draw()
        rec.draw()

        glViewport(int(x),int(y),int(self.window.width*0.20),int(self.window.height*0.30))

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        #gluPerspective(15, self.window.width/self.window.height, 1, 500)
        #gluPerspective(35, self.window.width/self.window.height, 1, self.maxlength)



        aspect_ratio = self.window.width / self.window.height

        # Fix vertical bounds
        half_height = 0.024 * self.window.height
        bottom = -half_height
        top = half_height

        # Adjust horizontal bounds based on aspect ratio
        half_width = half_height * aspect_ratio*0.60
        left = -half_width
        right = half_width
        near,far = -100,100
        glOrtho(left,right,bottom,top,near,far)



        glMatrixMode(GL_MODELVIEW)

        glPushMatrix()
        glLoadIdentity()
        #glTranslatef(0,0,0)
        #glTranslatef(-107.5,-49,0)

        #glPushMatrix()
        self.rotation_matrix = self.extract_rotation_matrix(self.matrix)
        glMultMatrixd(self.rotation_matrix)
        
        
        
        
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
        radius = 0.075
        length = 22
        opacity = 0.50
        # Create a GLU quadric object
        quadric = gluNewQuadric()
        # X-axis (Red)
        glColor4f(1, 0, 0, opacity)
        glPushMatrix()
        glTranslatef(0, 0, 0)
        glRotatef(90, 0, 1, 0)  # Rotate 90 degrees around the Y axis to align the cylinder along the X axis
        gluCylinder(quadric, radius, radius, length, 100, 100)
        glPopMatrix()

        #Boule au milieu
        """glColor4f(1, 1, 1, opacity)
        glPushMatrix()
        quadric = gluNewQuadric()
        gluSphere(quadric, 2*radius, 30, 30)
        glPopMatrix()"""

        # Z-axis (Vert)
        glColor4f(0, 1, 0, opacity)
        glPushMatrix()
        glTranslatef(0, 0, 0)
        glRotatef(180, 1, 0, 0)
        gluCylinder(quadric, radius, radius, length, 100, 100)  # No need for rotation as it's already aligned to the Y axis
        glPopMatrix()
                
        

        # Y-axis (Bleu)
        glColor4f(0, 0, 1, opacity)
        glPushMatrix()
        glTranslatef(0, 0, 0)
        glRotatef(-90, 1, 0, 0)  # Rotate -90 degrees around the X axis to align the cylinder along the Z axis
        gluCylinder(quadric, radius, radius, length, 100, 100)
        glPopMatrix()
        if self.axesEnable:
            length = length/2
            # Y-axis (Bleu)
            glColor4f(0, 0, 1, opacity*0.5)
            glPushMatrix()
            glTranslatef(0, 0, 0)
            glRotatef(90, 1, 0, 0)  # Rotate -90 degrees around the X axis to align the cylinder along the Z axis
            gluCylinder(quadric, radius, radius, length, 100, 100)
            glPopMatrix()
            #Z Axis (Vert)
            glColor4f(0, 1, 0, opacity*0.5)
            glPushMatrix()
            glTranslatef(0, 0, 0)
            gluCylinder(quadric, radius*0.75, radius*0.75, length, 100, 100)  # No need for rotation as it's already aligned to the Y axis
            glPopMatrix()
            #X-Axis (Rouge)
            glColor4f(1, 0, 0, opacity*0.5)
            glPushMatrix()
            glTranslatef(0, 0, 0)
            glRotatef(-90, 0, 1, 0)  # Rotate 90 degrees around the Y axis to align the cylinder along the X axis
            gluCylinder(quadric, radius*0.75, radius*0.75, length, 100, 100)
            glPopMatrix()
            glColor4f(1, 1, 1, 1)



            length = length*2
            nbre_line = 6
            position = [0,0,0]
            glBegin(GL_LINES)
            grid_spacing = length/nbre_line
            glColor4f(1,1,1,0.1)
            for i in range(0, nbre_line+1):
                offset = i * grid_spacing
                if i == nbre_line:
                    glColor4f(1,1,1,0.3)

                # Grid lines parallel to X-axis (both positive and negative Z direction)
                glVertex3f(position[0] - length, position[1], position[2] + offset)
                glVertex3f(position[0] + length, position[1], position[2] + offset)
                
                glVertex3f(position[0] - length, position[1], position[2] - offset)
                glVertex3f(position[0] + length, position[1], position[2] - offset)

                # Grid lines parallel to Z-axis (both positive and negative X direction)
                glVertex3f(position[0] + offset, position[1], position[2] - length)
                glVertex3f(position[0] + offset, position[1], position[2] + length)
                
                glVertex3f(position[0] - offset, position[1], position[2] - length)
                glVertex3f(position[0] - offset, position[1], position[2] + length)
            glEnd()
        glColor4f(1,1,1,1)

        glEnable(GL_TEXTURE_2D)
        scale = 4
        scale_radius = 5
        for obj in self.objects:
            glBindTexture(GL_TEXTURE_2D, obj.texture.id)
            glPushMatrix()
            position_minimap = self.scale_minimap_position(obj.position_simulation,length)
            glTranslatef(position_minimap[0], position_minimap[1], position_minimap[2])
            glRotatef(obj.rotation_siderale_angle,*obj.rotation_direction)
            quadric = gluNewQuadric()
            gluQuadricTexture(quadric, GL_TRUE)
            gluSphere(quadric, radius*10, 30, 30)
            glPopMatrix()
        glDisable(GL_TEXTURE_2D)

        if self.selectedObject is not None:
            glColor4f(0.3,1,0.3,0.4)
            glPushMatrix()
            position_minimap = self.scale_minimap_position(self.selectedObject.position_simulation,length)
            glTranslatef(position_minimap[0], position_minimap[1], position_minimap[2])
            quadric = gluNewQuadric()
            gluSphere(quadric, radius*18, 30, 30)
            glPopMatrix()

        glColor4f(1,1,1,1)



        # Delete the quadric object when done
        glColor4f(1, 1, 1, 1)
        gluDeleteQuadric(quadric)


        glDisable(GL_BLEND)
        #glPopMatrix()
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glDisable(GL_DEPTH_TEST)
        glViewport(0,0,self.window.width,self.window.height)

    def scale_minimap_position(self,position,length):
        # Convert Cartesian to Spherical
        x, y, z = position
        r = np.sqrt(x**2 + y**2 + z**2)
        theta = np.arctan2(y, x)
        phi = np.arccos(z / r) if r != 0 else 0
        
        # Scale the radial distance
        k = 0.08
        r_scaled = length * (np.log(1 + k * r) / np.log(1 + k * self.maxlength))
        
        # Convert Spherical back to Cartesian
        x_scaled = r_scaled * np.sin(phi) * np.cos(theta)
        y_scaled = r_scaled * np.sin(phi) * np.sin(theta)
        z_scaled = r_scaled * np.cos(phi)
        
        return [x_scaled, y_scaled, z_scaled]


    def extract_rotation_matrix(self,matrix):
        """
        Extract the rotational component from a 4x4 matrix.
        """
        rotation_only_matrix = (ctypes.c_double*16)()

        
        # Copy the rotational components (3x3 upper-left corner)
        rotation_only_matrix[0] = matrix[0]
        rotation_only_matrix[1] = matrix[1]
        rotation_only_matrix[2] = matrix[2]
        
        rotation_only_matrix[4] = matrix[4]
        rotation_only_matrix[5] = matrix[5]
        rotation_only_matrix[6] = matrix[6]
        
        rotation_only_matrix[8] = matrix[8]
        rotation_only_matrix[9] = matrix[9]
        rotation_only_matrix[10] = matrix[10]
        
        # Set the homogeneous coordinates to make it a valid 4x4 matrix
        rotation_only_matrix[15] = 1.0
        
        return rotation_only_matrix



    def setup_2d_projection(self):
        glDisable(GL_DEPTH_TEST)
        glViewport(0, 0, self.window.width, self.window.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.window.width, 0, self.window.height)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()


    def setup_3d_projection(self):
        glViewport(0, 0, self.window.width, self.window.height)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(35, self.window.width/self.window.height, 1, self.maxlength*2)
        glMatrixMode(GL_MODELVIEW)

    


    def set_background(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.background_texture.id)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(0, 0)
        glTexCoord2f(1, 0)
        glVertex2f(self.window.width, 0)
        glTexCoord2f(1, 1)
        glVertex2f(self.window.width, self.window.height)
        glTexCoord2f(0, 1)
        glVertex2f(0, self.window.height)
        glEnd()
        glDisable(GL_TEXTURE_2D)
    
    def set_background_test(self):
        glEnable(GL_TEXTURE_2D)

        rotation_offset_x = self.rotation_y*0.01
        rotation_offset_y = -self.rotation_x*0.01



        offset_x1 = self.translation_x * 0.01 + rotation_offset_x
        offset_y1 = self.translation_y * 0.01 + rotation_offset_y

        glBindTexture(GL_TEXTURE_2D, self.bg_texture2.id)
        self.draw_quad_with_offset(offset_x1,offset_y1)

        offset_x2 = self.translation_x * 0.05 + rotation_offset_x
        offset_y2 = self.translation_y * 0.05 + rotation_offset_y
        
        glBindTexture(GL_TEXTURE_2D, self.bg_texture2.id)
        self.draw_quad_with_offset(offset_x2,offset_y2,2)


        offset_x3 = self.translation_x * 2 - rotation_offset_x*20
        offset_y3 = self.translation_y * 2 - rotation_offset_y*20

        glBindTexture(GL_TEXTURE_2D, self.background_texture.id)
        self.draw_quad_with_offset(offset_x3,offset_y3,2)

    




        glDisable(GL_TEXTURE_2D)


    def draw_quad_with_offset(self, offset_x, offset_y, zoom_factor=1.0):
        # Calculate the zoomed dimensions
        zoomed_width = self.window.width * zoom_factor
        zoomed_height = self.window.height * zoom_factor

        # Calculate the difference to adjust the vertices
        diff_width = (self.window.width - zoomed_width) / 2
        diff_height = (self.window.height - zoomed_height) / 2

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


    
    def move_camera(self):
        
        if self.followObjectEnabled and self.followObject is not None:
            x_followObject = self.followObject.position_simulation[0]
            y_followObject = self.followObject.position_simulation[1]
            z_followObject = self.followObject.position_simulation[2]
        else:
            x_followObject,y_followObject,z_followObject = 0,0,0

        glLoadIdentity()
        #Translation initiale + Zoom
        #Translation selon le mouvement
        glTranslatef(self.translation_x,self.translation_y,0)
        glTranslatef(self.translation_initiale[0], self.translation_initiale[1], self.translation_initiale[2]+self.zoom)
        glRotatef(0, 1, 0, 0)  # Rotation autour de l'axe X
        glRotatef(self.rotation_y+self.rotation_initiale[1], 0, 1, 0)
        glRotatef(self.rotation_x+self.rotation_initiale[2], 0, 0, 1)
        glRotatef(self.rotation_z, 1, 0, 0)
    

        glTranslatef(- x_followObject,- y_followObject,-z_followObject)

        #Rotation selon le mouvement
        self.matrix = (GLdouble*16)()
        glGetDoublev(GL_MODELVIEW_MATRIX,self.matrix)

    def draw_pyglet_objects(self):
        for label in self.labels:
            label.draw()
        for btn in self.buttons:
            btn.update_position()
            btn.draw()
    

    def selection_mode(self,x,y,mode=0,liste_objects=[]):

        self.frameBuffer.bind()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


        self.render_with_colors()
        self.render_minimap_with_colors()
        if self.SimulationState.isCreating and mode == 1:
            self.render_creation_with_colors(liste_objects)

        output_buffer = (GLubyte*3)()

        glReadPixels(x,y,1,1,GL_RGB,GL_UNSIGNED_BYTE,output_buffer)

        self.frameBuffer.unbind()
        glClearColor(1,1,1, 1)
        glColor3f(1,1,1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        color_id = (output_buffer[0],output_buffer[1],output_buffer[2])


        if mode == 0:
            if color_id ==(0, 0, 50):#X
                self.SimulationState.focus_on_axes("x")
            elif color_id ==(0, 0, 150):#Y
                self.SimulationState.focus_on_axes("y")
            elif color_id ==(0, 0, 100):#Z
                self.SimulationState.focus_on_axes("z")
            if color_id[2]>200 : return None

            self.selectedObject = self.get_object_by_color_id(color_id, self.objects)

            return self.selectedObject
        elif mode == 1:
            return  self.get_object_by_color_id(color_id, liste_objects)

        
    def render_with_colors(self):
        # Clear the buffer with the blue background color
        glClearColor(0, 0, 1, 1)  # RGB for blue
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Setup 3D for drawing celestial objects
        self.setup_3d_projection()

        # Move the camera according to direction
        self.move_camera()

        # Now, for each object in your scene, set the color and draw it
        for obj in self.objects:
            # Extract the color_id (assuming it's in 0-255 range)
            r, g, b = obj.color_id

            # Convert the color to 0-1 range
            r /= 255.0
            g /= 255.0
            b /= 255.0

            # Set the color for the object
            glColor3f(r, g, b)
            # Draw the object using the same transformations but with the unique color
            glPushMatrix()
            glTranslatef(obj.position_simulation[0], obj.position_simulation[1], obj.position_simulation[2])
            if hasattr(obj, "inclinaison"):
                glRotatef(obj.inclinaison, 1, 0, 0)
            #glRotatef(obj.rotation_siderale_angle, *obj.rotation_direction)
            quadric = gluNewQuadric()
            gluSphere(quadric, obj.rayon_simulation, 60, 18)
            glPopMatrix()

    def render_minimap_with_colors(self):
        glViewport(int(self.window.width * 0.01), int(self.window.height * 0.02), int(self.window.width * 0.20), int(self.window.height * 0.30))
        
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        
        aspect_ratio = self.window.width / self.window.height


        # Fix vertical bounds
        half_height = 0.024 * self.window.height  # valeur mise à jour
        bottom = -half_height
        top = half_height


        # Ajuster les limites horizontales en fonction du rapport d'aspect
        half_width = half_height * aspect_ratio*0.60
        left = -half_width
        right = half_width
        near, far = -100, 100
        glOrtho(left, right, bottom, top, near, far)


        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glTranslatef(0, 0, 0)
        
        self.rotation_matrix = self.extract_rotation_matrix(self.matrix)
        glMultMatrixd(self.rotation_matrix)
        
        radius = 1
        length = 22
        quadric = gluNewQuadric()  # If you don't have this, add it at the beginning
    
        # X-axis (Red)
        glColor3f(0, 0, 50/255.0)  # RGB for X axis color
        glPushMatrix()
        glTranslatef(0, 0, 0)
        glRotatef(90, 0, 1, 0)  # Rotate 90 degrees around the Y axis to align the cylinder along the X axis
        gluCylinder(quadric, radius, radius, length, 100, 100)
        glPopMatrix()

        # Z-axis (Green)
        glColor3f(0, 0, 100/255.0)  # RGB for Z axis color
        glPushMatrix()
        glTranslatef(0, 0, 0)
        glRotatef(180, 1, 0, 0)
        gluCylinder(quadric, radius, radius, length, 100, 100)  # No need for rotation as it's already aligned to the Y axis
        glPopMatrix()

        # Y-axis (Blue)
        glColor3f(0, 0, 150/255.0)  # RGB for Y axis color
        glPushMatrix()
        glTranslatef(0, 0, 0)
        glRotatef(-90, 1, 0, 0)  # Rotate -90 degrees around the X axis to align the cylinder along the Z axis
        gluCylinder(quadric, radius, radius, length, 100, 100)
        glPopMatrix()


        radius = 0.075*2
        # Effacer le tampon
        glClearColor(0, 0, 1, 1)  # RGB pour bleu
        #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for obj in self.objects:
            r, g, b = obj.color_id


            # Convertir la couleur à la plage 0-1
            r /= 255.0
            g /= 255.0
            b /= 255.0


            # Définir la couleur pour l'objet
            glColor3f(r, g, b)
            glPushMatrix()
            position_minimap = self.scale_minimap_position(obj.position_simulation, length)
            glTranslatef(position_minimap[0], position_minimap[1], position_minimap[2])
            quadric = gluNewQuadric()
            gluSphere(quadric, radius * 10, 30, 30)
            glPopMatrix()
        
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glViewport(0, 0, self.window.width, self.window.height)

    def render_creation_with_colors(self,objects):
        self.setup_2d_projection()
        self.padding=5
        self.width = self.window.width
        self.height = self.window.height
        self.x = int(0.01 * self.width)
        self.y = int(0.38 * self.height)

        self.largeur = int(0.20*self.width)
        self.hauteur = int(0.5*self.height)
        glViewport(self.x + self.padding, self.y + self.padding, self.largeur - 2 * self.padding, self.hauteur - 2 * self.padding)
           
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        fov = 35
        aspect_ratio = (self.largeur - 2 * self.padding) / (self.hauteur - 2 * self.padding)
        near = 0.1
        far = 100
        gluPerspective(fov, aspect_ratio, near, far)

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

        for obj in objects:
            r, g, b = obj.color_id
            r /= 255.0
            g /= 255.0
            b /= 255.0
            glColor3f(r, g, b)
            glPushMatrix()

            # Translation to position the planet
            glTranslatef(start_x + col_count * (gap + 2 * planet_radius), start_y - row_count * (gap + 2 * planet_radius), -100)
            quadric = gluNewQuadric()
            gluSphere(quadric, planet_radius, 100, 30)

            glPopMatrix()

            # Update counters to position the next planet
            col_count += 1
            if col_count == num_planets_per_row:
                col_count = 0
                row_count += 1
    
        # Restore the previous projection
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glViewport(0, 0, self.width, self.height)
        self.setup_3d_projection()
    
    def is_color_close(self, color1, color2, threshold=10):
        """Check if two colors are close based on a threshold."""
        return all(abs(c1 - c2) <= threshold for c1, c2 in zip(color1, color2))

    def get_object_by_color_id(self, color_id,object_list ,threshold=10):
        for obj in object_list:
            if self.is_color_close(obj.color_id, color_id, threshold):
                return obj
        return None


    def draw_planet_path(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        #glEnable(GL_LINE_SMOOTH)
        #glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)

        for obj in self.objects:
            if obj.drawOrbitEnable and len(obj.position_history) > 2:
                glLineWidth(0.5) 
                glBegin(GL_LINE_STRIP)
                path_length = len(obj.position_history)  # Define the path_length here
                for index, position in enumerate(obj.position_history):
                    alpha = 0.75*(index / (path_length - 1))
                    glColor4f(1, 1, 1, alpha)
                    glVertex3f(position[0], position[1], position[2])
                glEnd()  # Ensure glEnd is called for each object's path

        glColor4f(1, 1, 1, 1)  # Reset color
        glLineWidth(1)         # Reset line width

    def draw_saturn_ring(self, obj):

        # Assuming obj represents Saturn and has attributes for ring texture, radius, and position.

        # Enable texture
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glBindTexture(GL_TEXTURE_2D, self.saturn_ring.id)

        # Enable blending for transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glPushMatrix()

        # Translate to Saturn's position
        glTranslatef(obj.position_simulation[0]+1, obj.position_simulation[1]+1, obj.position_simulation[2])

        # Rotate for inclination of the rings
        glRotatef(20, 1, 0, 0)

        half_width = obj.rayon_simulation * 2.5  # or whatever appropriate size
        half_height = half_width  # since it's square

        # Draw a textured quad for the ring
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex3f(-half_width, -half_height, 0)
        glTexCoord2f(1, 0); glVertex3f( half_width, -half_height, 0)
        glTexCoord2f(1, 1); glVertex3f( half_width,  half_height, 0)
        glTexCoord2f(0, 1); glVertex3f(-half_width,  half_height, 0)
        glEnd()

        glPopMatrix()




    def draw_axes(self, length=50, position = [0,0,0]):
        nbre_line = 20
        glBegin(GL_LINES)
        length = self.maxlength

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
        if not self.axesDrawned:
            dynamic_offset_factor = self.frame_counter_axes/temps
            self.frame_counter_axes+=1
            if self.frame_counter_axes >= temps:
                self.axesDrawned = True
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

    def follow_line(self,position):
        glBegin(GL_LINES)
        glColor4f(1,1,1,0.6)
        #Lign from the sun to the object
        if self.followLineEnable:
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
        rec = shapes.Rectangle(self.window.width * x, self.window.height * y, self.window.width * largeur, self.window.height * hauteur, color=(41, 50, 69)) 
        rec2 = shapes.Rectangle(self.window.width * x - padding / 2, self.window.height * y - padding / 2, self.window.width * largeur + padding, self.window.height * hauteur + padding, color=(255, 255, 255)) 
        rec.opacity = 120 
        rec2.opacity = 20
        # Dessinez l'écriture
        centrer_x = (self.window.width * (x + largeur / 2))/self.window.width
        centrer_y = (self.window.height * (y + hauteur - 0.035))/self.window.height
        # Configurez le viewport pour les rectangles
    

        # Dessinez les rectangles directement sans aucune modification de la projection
        rec2.draw()
        rec.draw()
        diff = 0.025
        hauteur_vitesse = 0.12
        type_object = self.type_object_celeste_mapping.get(object.type_object)
        couleur_type_object = self.type_object_celeste_mapping_color.get(object.type_object)
        Label(self.window.get_size(), f'{object.name}', centrer_x, centrer_y, self.font, (255, 255, 255, 200), 2.5).draw()
        Label(self.window.get_size(), f'{type_object}', centrer_x, centrer_y-0.035, self.font, couleur_type_object, 1.5).draw()
        Label(self.window.get_size(), "Vitesse", centrer_x, centrer_y-0.10, self.font, (255,255,255,200), 1.5).draw()
        Label(self.window.get_size(), f"{object.get_velocity():,.0f} km/h".replace(",", ' '), centrer_x, centrer_y-0.125, self.font, (255,255,255,150), 1.2).draw()

        Label(self.window.get_size(), "Masse", centrer_x, centrer_y-0.160, self.font, (255,255,255,200), 1.5).draw()
        Label(self.window.get_size(), f"{object.weight:,.2e} kg".replace(",", ' '), centrer_x, centrer_y-0.160-diff, self.font, (255,255,255,150), 1.2).draw()

        Label(self.window.get_size(), "Rayon", centrer_x, centrer_y-0.155-diff-0.05, self.font, (255,255,255,200), 1.5).draw()
        Label(self.window.get_size(), f"{object.real_radius:,.0f} km".replace(",", ' '), centrer_x, centrer_y-0.155-2*diff-0.05, self.font, (255,255,255,150), 1.2).draw()

        if object.type_object !=1:
            Label(self.window.get_size(), "Force gravitationnelle", centrer_x, centrer_y-0.155-2*diff-2*0.05, self.font, (255,255,255,200), 1.5).draw()
            Label(self.window.get_size(), f"{object.get_force():,.2e} N".replace(",", ' '), centrer_x, centrer_y-0.155-3*diff-2*0.05, self.font, (255,255,255,150), 1.2).draw()
        else:
            Label(self.window.get_size(), "Température", centrer_x, centrer_y-0.155-2*diff-2*0.05, self.font, (255,255,255,200), 1.5).draw()
            Label(self.window.get_size(), f"5 500 k".replace(",", ' '), centrer_x, centrer_y-0.155-3*diff-2*0.05, self.font, (255,255,255,150), 1.2).draw()


        glViewport(int(self.window.width * x), int(self.window.height * y), int(self.window.width * largeur), int(self.window.height * hauteur))
        # Configurez la projection pour le rendu 3D
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        fov = 35
        aspect_ratio = (self.window.width * largeur) / (self.window.height * hauteur)
        near = 0.1
        far = 100
        gluPerspective(fov, aspect_ratio, near, far)

        # Dessinez la sphère
        glEnable(GL_TEXTURE_2D)
        glPushMatrix()
        # Placez la caméra un peu plus loin pour voir correctement la sphère
        glTranslatef(0, -19.5, -100)
        #glRotatef(90,1,0,0)
        self.rotation_matrix = self.extract_rotation_matrix(self.matrix)
        glMultMatrixd(self.rotation_matrix)
        glBindTexture(GL_TEXTURE_2D, object.texture.id)
        glRotatef(self.selectedObject.rotation_siderale_angle,*self.selectedObject.rotation_direction)
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
        glViewport(0, 0, self.window.width, self.window.height)










    def draw_highlight(self, obj):
        scale_factor = 0.5 * math.sin(2 * math.pi * self.frame_counter / 90) + 0.5  # This oscillates between 0 and 1 over 60 frames
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
        for i in range(1,50):
            glColor4f(1.0,1.0,1,(0.04+scale_factor/20)/(i))
            gluSphere(quad,obj.rayon_simulation*(1+0.02*i),100,100)
        gluDeleteQuadric(quad)


        glPopMatrix()
        glColor4f(1, 1, 1, 1)

    def draw_sun(self, obj):
        quadric = gluNewQuadric()
        gluQuadricTexture(quadric, GL_TRUE)
        gluSphere(quadric, obj.rayon_simulation, 100, 30)
        glPopMatrix()

        glDisable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
        glDisable(GL_DEPTH_TEST)

        glPushMatrix()
        quadric = gluNewQuadric()

        for i in range(1,30):
            glColor4f(1.0,1.0,0.8,0.06/i)
            gluSphere(quadric,obj.rayon_simulation*(1+0.0125*i),100,30)
        glPopMatrix()
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_BLEND)
        glEnable(GL_TEXTURE_2D)
        glColor4f(1,1,1,1)
    
        

    def draw_celestial_objects(self):
        glEnable(GL_TEXTURE_2D)
        # Set up lighting parameters
        
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)


        ambient_light_intensity = 20
        ambient_light = (GLfloat * 4)(ambient_light_intensity/100, ambient_light_intensity/100, ambient_light_intensity/100, 1.0) # Ambient reflection 
        glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_light) 

        diffuse_light_intensity = 100
        diffuse_light = (GLfloat * 4)(diffuse_light_intensity/100, diffuse_light_intensity/100, diffuse_light_intensity/100, 1.0) # Diffuse reflection 
        glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse_light) 

        specular_light_intensity = 100
        specular_light = (GLfloat * 4)(specular_light_intensity/100, specular_light_intensity/100, specular_light_intensity/100, 1.0) # Specular reflection 
        glLightfv(GL_LIGHT0, GL_SPECULAR, specular_light)
        

        for i,obj in enumerate(self.objects):
            #Bind texture
            glBindTexture(GL_TEXTURE_2D, obj.texture.id)
            glPushMatrix()
            #On positionne l'object
            glTranslatef(obj.position_simulation[0], obj.position_simulation[1], obj.position_simulation[2])
            if hasattr(obj, "inclinaison"):
                glRotatef(obj.inclinaison,1,0,0)
    
            glRotatef(obj.rotation_siderale_angle,*obj.rotation_direction)

            if obj.type_object == 1: #Une étoile
                sun_position = (GLfloat*4)(obj.position_simulation[0], obj.position_simulation[1], obj.position_simulation[2], 1)
                glLightfv(GL_LIGHT0, GL_POSITION, sun_position)

                glDisable(GL_LIGHTING)

                self.draw_sun(obj)

                glEnable(GL_LIGHTING)





            else:
                
                #On dessine une sphère avec la texture
                quadric = gluNewQuadric()
                gluQuadricTexture(quadric, GL_TRUE)
                gluSphere(quadric, obj.rayon_simulation, 100, 30)
                glPopMatrix()


            #Anneaux de Saturne
            if obj.name == "Saturne":
                self.draw_saturn_ring(obj)



        glDisable(GL_TEXTURE_2D)
        glDisable(GL_LIGHTING)
        glDisable(GL_LIGHT0)  
    


    def draw(self):

        #Setup 2D + Fond d'écran
        self.setup_2d_projection()
        self.set_background_test()

        #Setup 3D pour dessiner les objects celestes
        self.setup_3d_projection()
        #Bouger la caméra selon la direction
        self.move_camera()

        #Dessiner les objects
        self.draw_celestial_objects()

         #Highlight selected object
        if self.selectedObject:
            self.draw_highlight(self.selectedObject)
            self.follow_line(self.selectedObject.position_simulation)
        if self.axesEnable:
            self.draw_axes()
        else:
            self.frame_counter_axes=0
        #Path of objects:
        self.draw_planet_path()

        #Remise en 2D
        self.setup_2d_projection()
        if self.selectedObject:self.draw_selected_object_infos(self.selectedObject)
        self.draw_minimap()
        if self.SimulationState.isCreating:
            self.SimulationState.OutilCreation.draw()


        #Dessiner bouttons + Labels
        self.draw_pyglet_objects()


        #self.frameBuffer.draw(0,0)

        self.frame_counter+=1
        if self.frame_counter>90:
            self.frame_counter = 0



