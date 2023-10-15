from pyglet.gl import *
from pyglet.text import Label
texture = pyglet.image.load('assets/textures/lunar.jpg').get_texture()
import math

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

        # Unbind
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def bind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)

    def unbind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)


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
        self.distance_initiale = -75

        #Initiate only
        self.background_texture = backgroundTexture
        self.frameBuffer = FrameBuffer(*window.get_size())

        #Status Conditions to False
        self.isSelected = False
    
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
        self.set_background()

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


        

    

