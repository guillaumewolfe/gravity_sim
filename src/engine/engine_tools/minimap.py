from pyglet.gl import *
from pyglet.text import Label
from pyglet import shapes
import math

class Minimap:
    def __init__(self,window):
        self.window = window
        self.x_rel = 0
        self.y_rel = 0
        self.width_rel = 0.25
        self.height_rel = 0.25

        self.rectangle_opacity = 150


    def update(self,window):
        self.window=window
        


    def draw_axes(self, length=100):
        # Draw X-axis (Red)
        glColor3f(1, 0, 0)
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(length, 0, 0)
        glEnd()

        # Draw Y-axis (Green)
        glColor3f(0, 1, 0)
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(0, length, 0)
        glEnd()

        # Draw Z-axis (Blue)
        glColor3f(0, 0, 1)
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, length)
        glColor3f(1, 1, 1)
        glEnd()

    def draw_background_rectangle(self,):
        rec  = shapes.Rectangle(0, 0, self.window.width*0.25, self.window.height*0.25, color=(255,0,0))
        rec.opacity = self.rectangle_opacity
        rec.draw()

    def draw(self):
        # ... (rest of the original draw method code)

        # Move to bottom corner
        glPushMatrix()
        glTranslatef(50, 50, 0)  # Translate to bottom left corner. Adjust these values if needed.

        # Draw background rectangle
        self.draw_background_rectangle()
        # Draw the axes
        self.draw_axes()

        glPopMatrix()
