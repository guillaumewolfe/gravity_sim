from pyglet.gl import *
from pyglet.text import Label
texture = pyglet.image.load('assets/textures/lunar.jpg').get_texture()
import math
from ctypes import byref

class FrameBuffer:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Generate frame buffer
        self.fbo = GLuint()
        glGenFramebuffers(1, self.fbo)
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)

        # Generate texture
        self.texture = GLuint()
        glGenTextures(1, self.texture)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glBindTexture(GL_TEXTURE_2D, 0)

        # Attach it to FBO
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.texture, 0)

        # Create the depth buffer
        self.depth_buffer = GLuint()
        glGenRenderbuffers(1, byref(self.depth_buffer))
        glBindRenderbuffer(GL_RENDERBUFFER, self.depth_buffer)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT24, width, height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self.depth_buffer)
        
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            print("Failed to create framebuffer!")


        # Unbind
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def bind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)

    def unbind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
    
    def draw(self, x, y):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(x, y)
        glTexCoord2f(1, 0); glVertex2f(x + self.width, y)
        glTexCoord2f(1, 1); glVertex2f(x + self.width, y + self.height)
        glTexCoord2f(0, 1); glVertex2f(x, y + self.height)
        glEnd()
        glDisable(GL_TEXTURE_2D)


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
        self.distance_initiale = -100

        #Initiate only
        self.background_texture = backgroundTexture
        self.frameBuffer = FrameBuffer(*window.get_size())

        #Status Conditions to False
        self.isSelected = False

        #Temporaire
        self.bg_texture1 = pyglet.image.load('assets/textures/background_alpha1.png').get_texture()
        self.bg_texture2 = pyglet.image.load('assets/textures/background2.jpg').get_texture()
    
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

        glBindTexture(GL_TEXTURE_2D, self.background_texture.id)
        self.draw_quad_with_offset(offset_x2,offset_y2,60)

        offset_x3 = self.translation_x * 0.06 + rotation_offset_x
        offset_y3 = self.translation_y * 0.06 + rotation_offset_y

        glBindTexture(GL_TEXTURE_2D, self.background_texture.id)
        self.draw_quad_with_offset(offset_x3,offset_y3,1)



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
        glLoadIdentity()
        #Translation initiale + Zoom
        glTranslatef(0, 0, self.distance_initiale+self.zoom)
        #Translation selon le mouvement
        glTranslatef(self.translation_x,self.translation_y,0)

        #Rotation selon le mouvement
        glRotatef(self.rotation_x, 1, 0, 0)  # Rotation autour de l'axe X
        glRotatef(self.rotation_y, 0, 1, 0)
        glRotatef(self.rotation_z, 0, 0, 1)
    
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
        print(color_id)



        if color_id[2]>200 : return None

        selected_obj = self.get_object_by_color_id(color_id)

        return selected_obj
    
        
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



    def draw_celestial_objects(self):
        for obj in self.objects:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, obj.texture.id)
            glPushMatrix()
            glTranslatef(obj.position_simulation[0], obj.position_simulation[1], obj.position_simulation[2])
            if hasattr(obj, "inclinaison"):
                glRotatef(obj.inclinaison,1,0,0)
    
            glRotatef(obj.rotation_siderale_angle,*obj.rotation_direction)

            quadric = gluNewQuadric()
            gluQuadricTexture(quadric, GL_TRUE)
            gluSphere(quadric, obj.rayon_simulation, 60, 18)
            glPopMatrix()
            glDisable(GL_TEXTURE_2D)
    
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

        #Remise en 2D
        self.setup_2d_projection()

        #Dessiner bouttons + Labels
        self.draw_pyglet_objects()

        #Dessiner les coordonnées de la caméra
        self.draw_camera_coordinates()

        #self.frameBuffer.draw(0,0)



            