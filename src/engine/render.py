from pyglet.gl import *
from pyglet.text import Label
texture = pyglet.image.load('assets/textures/lunar.jpg').get_texture()
import math

def setup_2d_projection(window):
    glDisable(GL_DEPTH_TEST)
    glViewport(0, 0, window.width, window.height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, window.width, 0, window.height)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def setup_3d_projection(window):
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(35, window.width/window.height, 1, 1000)
    glMatrixMode(GL_MODELVIEW)


def draw_sphere(window):
    glLoadIdentity()
    glTranslatef(0, 0, 0)
    # Activer la texture
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture.id)
    
    # Dessiner la sphère avec la texture
    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)  # Indique à gluSphere d'utiliser des coordonnées de texture
    gluSphere(quadric, 0.75, 60, 18)  # J'ai réduit le rayon à 0.5 pour que la sphère soit plus petite

    # Désactiver la texture
    glDisable(GL_TEXTURE_2D)

def draw_object_with_texture(window, obj):
    # Activez la texture de l'objet
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, obj.texture.id)
    # Code pour dessiner l'objet avec sa texture
    # (par exemple, si c'est une sphère, vous utiliseriez gluSphere)
    glPushMatrix()
    glTranslatef(obj.position_simulation[0], obj.position_simulation[1], obj.position_simulation[2])
    if hasattr(obj, "inclinaison"):
        glRotatef(obj.inclinaison,1,0,0)
    
    glRotatef(obj.rotation_siderale_angle,*obj.rotation_direction)

    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    gluSphere(quadric, obj.rayon_simulation, 60, 18)
    glPopMatrix()

    # Désactivez la texture pour d'autres rendus
    glDisable(GL_TEXTURE_2D)

def calculate_camera_vectors(rotation_x, rotation_y):
    # Supposons que les vecteurs sont à une distance fixe de la caméra (par exemple, 2 unités)
    distance = 1.0

    # Convertissez les rotations en radians
    rotation_x_rad = math.radians(rotation_x)
    rotation_y_rad = math.radians(rotation_y)

    # Calculez les coordonnées dans l'espace de la caméra en utilisant les angles de rotation
    camera_x = distance * math.sin(rotation_y_rad) * math.cos(rotation_x_rad)
    camera_y = -distance * math.sin(rotation_x_rad)
    camera_z = -distance * math.cos(rotation_y_rad) * math.cos(rotation_x_rad)

    return camera_x, camera_y, camera_z

def set_background(window,background_texture):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, background_texture.id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(0, 0)
    glTexCoord2f(1, 0)
    glVertex2f(window.width, 0)
    glTexCoord2f(1, 1)
    glVertex2f(window.width, window.height)
    glTexCoord2f(0, 1)
    glVertex2f(0, window.height)
    glEnd()
    glDisable(GL_TEXTURE_2D)






def draw_objects(window, labels, buttons, objects, rotation_x, rotation_y, rotation_z, translation_x,translation_y,zoom,background_texture):
    # Configuration pour le rendu 2D
    camera_x, camera_y, camera_z = calculate_camera_vectors(rotation_x, rotation_y)
    setup_2d_projection(window)

    # Dessiner le fond d'écran 2D en premier
    set_background(window, background_texture)


    # Configuration pour le rendu 3D
    setup_3d_projection(window)
    glLoadIdentity()
    glTranslatef(0, 0, -75+zoom)  # Déplacez la caméra un peu plus loin


    glTranslatef(translation_x,translation_y,0)


    glRotatef(rotation_x, 1, 0, 0)  # Rotation autour de l'axe X
    glRotatef(rotation_y, 0, 1, 0)
    glRotatef(rotation_z, 0, 0, 1)

    for obj in objects:
        draw_object_with_texture(window, obj)

    # Configuration pour le rendu 2D pour dessiner les labels
    setup_2d_projection(window)
        # Dessiner les boutons et autres éléments 2D
    for label in labels:
        label.draw()
    for btn in buttons:
        btn.update_position()
        btn.draw()
    
    # Calculez les coordonnées des vecteurs dans l'espace de la caméra

    # Ajoutez les labels des vecteurs en bas à droite
    label_x = Label(f'X: {camera_x:.2f}', font_name='Arial', font_size=12, x=window.width - 200, y=10, anchor_x='right', anchor_y='bottom', color=(255, 255, 255, 255))
    label_y = Label(f'Y: {camera_y:.2f}', font_name='Arial', font_size=12, x=window.width - 120, y=10, anchor_x='right', anchor_y='bottom', color=(255, 255, 255, 255))
    label_z = Label(f'Z: {camera_z:.2f}', font_name='Arial', font_size=12, x=window.width - 40, y=10, anchor_x='right', anchor_y='bottom', color=(255, 255, 255, 255))
    label_x.draw()
    label_y.draw()
    label_z.draw()
