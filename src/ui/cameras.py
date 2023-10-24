from pyglet.gl import gluLookAt, glLoadIdentity, glScalef, glRotatef, glTranslatef
import math

class Camera:
    def __init__(self, x, y, z, target_x, target_y, target_z):
        self.x = x
        self.y = y
        self.z = z
        self.target_x = target_x
        self.target_y = target_y
        self.target_z = target_z

        self.zoom = 1.0
        self.translate = [0, 0, 0]
        self.rotate = [0, 0, 0]

    def apply_transformations(self):
        # 1. Translatez la caméra pour la position de l'objet que vous suivez
        glTranslatef(self.target_x, self.target_y, self.target_z)

        # 2. Appliquez les rotations autour des axes X, Y et Z
        glRotatef(self.rotate[0], 1, 0, 0)
        glRotatef(self.rotate[1], 0, 1, 0)
        glRotatef(self.rotate[2], 0, 0, 1)

        # 3. Translatez la caméra à sa position d'origine
        glTranslatef(-self.target_x, -self.target_y, -self.target_z)

        # Appliquez d'autres transformations (zoom, translation, etc.) si nécessaire
        glTranslatef(self.translate[0], self.translate[1], self.translate[2])


    def look_at(self):
        self.update_position()
        self.apply_transformations() # Réinitialisez la matrice de modèle-vue
        gluLookAt(self.x, self.y, self.z,
                  self.target_x, self.target_y, self.target_z,
                  0, 1, 0)

    def update_position(self):
        pass

    def reset(self):
        self.zoom = 1.0
        self.translate = [0, 0, 0]
        self.rotate = [0, 0, 0]

class CameraX(Camera):
    def update_position(self):
        self.x = self.target_x-200
        self.y = self.target_y 
        self.z = self.target_z

class CameraY(Camera):
    def update_position(self):
        self.x = self.target_x
        self.y = self.target_y -10
        self.z = self.target_z

class CameraZ(Camera):
    def update_position(self):
        self.x = self.target_x
        self.y = self.target_y
        self.z = self.target_z - 100

class CameraIso(Camera):
    def __init__(self, x, y, z, target_x, target_y, target_z):
        super().__init__(x, y, z, target_x, target_y, target_z)

    def look_at(self):
        super().look_at()
        self.update_position()
        gluLookAt(self.x, self.y, self.z,
                  self.target_x, self.target_y, self.target_z,
                  0, 1, 0)

    def update_position(self):
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dz = self.target_z - self.z
        distance = math.sqrt(dx**2 + dy**2 + dz**2)

        self.x = self.target_x - 10 * dx / distance
        self.y = self.target_y - 10 * dy / distance
        self.z = self.target_z - 10 * dz / distance

class CameraOrbit(Camera):
    def __init__(self, x, y, z, target, theta):
        super().__init__(x, y, z, target[0], target[1], target[2])
        self.target = target
        self.theta = theta

    def update_position(self):
        self.x = self.target[0] + 10 * math.cos(self.theta)
        self.y = self.target[1]
        self.z = self.target[2] + 10 * math.sin(self.theta)
        self.theta += 0.01  # Ajustez pour contrôler la vitesse de rotation
        if self.theta > 2 * math.pi:
            self.theta -= 2 * math.pi
