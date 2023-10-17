from pyglet.gl import *
from pyglet.text import Label
import math
from engine_tools.FrameBuffer import FrameBuffer
from ctypes import c_char_p,POINTER,c_int,cast

class RenderTool:
    def __init__(self,window, labels, buttons, objects, rotation_x, rotation_y, rotation_z, translation_x,translation_y,zoom,backgroundTexture):
        #Fenêtre
        self.window = window
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
        self.planeEnable = True
        self.followLineEnable = True



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



    def setup_2d_projection(self):
        glDisable(GL_DEPTH_TEST)
        glViewport(0, 0, self.window.width, self.window.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.window.width, 0, self.window.height)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()


    def setup_3d_projection(self):
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(35, self.window.width/self.window.height, 1, 1000)
        glMatrixMode(GL_MODELVIEW)

    def calculate_camera_vectors(self):
        # Supposons que les vecteurs sont à une distance fixe de la caméra (par exemple, 2 unités)
        distance = 1.0

        # Convertissez les rotations en radians
        rotation_x_rad = math.radians(self.rotation_x)
        rotation_y_rad = math.radians(self.rotation_y)

        # Calculez les coordonnées dans l'espace de la caméra en utilisant les angles de rotation
        camera_x = distance * math.sin(rotation_y_rad) * math.cos(rotation_x_rad)
        camera_y = -distance * math.sin(rotation_x_rad)
        camera_z = -distance * math.cos(rotation_y_rad) * math.cos(rotation_x_rad)

        return camera_x, camera_y, camera_z
    


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


        offset_x3 = self.translation_x * 2 + rotation_offset_x*20
        offset_y3 = self.translation_y * 2 + rotation_offset_y*20

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
    

        glTranslatef(- x_followObject,- y_followObject,-z_followObject)

        #Rotation selon le mouvement

    def draw_pyglet_objects(self):
        for label in self.labels:
            label.draw()
        for btn in self.buttons:
            btn.update_position()
            btn.draw()
    
    def draw_camera_coordinates(self):
        camera_x, camera_y, camera_z = self.calculate_camera_vectors()
        label_x = Label(f'X: {camera_x:.2f}', font_name='Arial', font_size=12, x=self.window.width - 200, y=10, anchor_x='right', anchor_y='bottom', color=(255, 255, 255, 255))
        label_y = Label(f'Y: {camera_y:.2f}', font_name='Arial', font_size=12, x=self.window.width - 120, y=10, anchor_x='right', anchor_y='bottom', color=(255, 255, 255, 255))
        label_z = Label(f'Z: {camera_z:.2f}', font_name='Arial', font_size=12, x=self.window.width - 40, y=10, anchor_x='right', anchor_y='bottom', color=(255, 255, 255, 255))
        label_x.draw()
        label_y.draw()
        label_z.draw()

    def selection_mode(self,x,y):

        self.frameBuffer.bind()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.render_with_colors()

        output_buffer = (GLubyte*3)()

        glReadPixels(x,y,1,1,GL_RGB,GL_UNSIGNED_BYTE,output_buffer)

        self.frameBuffer.unbind()
        glClearColor(1,1,1, 1)
        glColor3f(1,1,1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        color_id = (output_buffer[0],output_buffer[1],output_buffer[2])



        if color_id[2]>200 : return None

        self.selectedObject = self.get_object_by_color_id(color_id)

        return self.selectedObject

        
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



   

    
    def is_color_close(self, color1, color2, threshold=10):
        """Check if two colors are close based on a threshold."""
        return all(abs(c1 - c2) <= threshold for c1, c2 in zip(color1, color2))

    def get_object_by_color_id(self, color_id, threshold=10):
        for obj in self.objects:
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

        glDisable(GL_TEXTURE_2D)
        glDisable(GL_LIGHTING)
        glDisable(GL_LIGHT0)


    def draw_axes(self, length=50, position = [0,0,0]):

        glEnable(GL_LINE_STIPPLE)
        basic_pattern = [0xAAAA,0xEAEA,0x5555,0x7575,0xAAAA,0xD5D5,0x5555,0xB5B5]
        index = int(self.frame_counter/5)%len(basic_pattern)
        stipple_pattern = basic_pattern[index]
        glLineStipple(4,stipple_pattern&0xFFFF)
        glLineStipple(4,0xAAAA)
        glDisable(GL_LINE_STIPPLE)


        glBegin(GL_LINES)

        glColor4f(1,1,1,0.5)


        if self.axesEnable:
            #Axe X
            glVertex3f(position[0],position[1],position[2])
            glVertex3f(position[0]+length,position[1],position[2])
            
            #Axe Z
            glVertex3f(position[0],position[1],position[2])
            glVertex3f(position[0],position[1],position[2]+length)
            
            #Axe Y
            glVertex3f(position[0],position[1],position[2])
            glVertex3f(position[0],position[1]+length,position[2])

        glColor4f(1,1,1,0.6)
        #Lign from the sun to the object
        if self.followLineEnable:
            glVertex3f(0,0,0)
            glVertex3f(position[0],position[1],position[2])


        glColor4f(1,1,1,1)
        glEnd()
        glDisable(GL_LINE_STIPPLE)



    def draw_highlight(self, obj):
        scale_factor = 0.5 * math.sin(2 * math.pi * self.frame_counter / 90) + 0.5  # This oscillates between 0 and 1 over 60 frames
        scale = obj.rayon_simulation *1.01 + 1.5 * scale_factor 
        position = obj.position_simulation
        """Draw a semi-transparent sphere around the selected object."""
        # Color (47,233,240) with 0.5 transparency
        colors = (255,255,255)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)

        glColor4f(colors[0]/255, colors[1]/255, colors[2]/255, 0.15)
        

        glPushMatrix()
        
        # Translate to the object's position
        glTranslatef(position[0], position[1], position[2])
        
        # Scale if necessary. You can adjust or remove this line depending on your needs.
        glScalef(scale, scale, scale)
        
        # Drawing the sphere (assuming you have the glu library with pyglet)
        quad = gluNewQuadric()
        gluSphere(quad, 1.0, 60, 60)
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

        for i in range(1,2):
            glColor4f(1.0,1.0,0.7,0.05/i)
            gluSphere(quadric,obj.rayon_simulation*(1+0.005*i),100,30)
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
            self.draw_axes(position=self.selectedObject.position_simulation)
        #Path of objects:
        self.draw_planet_path()


        #Remise en 2D
        self.setup_2d_projection()

        #Dessiner bouttons + Labels
        self.draw_pyglet_objects()

        #Dessiner les coordonnées de la caméra
        self.draw_camera_coordinates()

        #self.frameBuffer.draw(0,0)

        self.frame_counter+=1
        if self.frame_counter>90:
            self.frame_counter = 0






            