import pyglet
from pyglet import shapes
from pyglet.gl import *
import states

def handle_input(window, current_state):
    @window.event
    def on_mouse_press(x, y, button, modifiers):
        current_state.on_mouse_press(x, y, button, modifiers)
        # ... (logique de gestion des entrées) ...

    @window.event
    def on_close():
        current_state.close_app()

    @window.event
    def on_resize(width, height):
        # Adjust viewport and projection
        current_state.draw()
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, width, 0, height)
        glMatrixMode(GL_MODELVIEW)
    @window.event
    def on_mouse_motion(x, y, dx, dy):
        for btn in current_state.buttons:
            if btn.contains_point(x, y):
                btn.hover = True
            else:
                btn.hover = False
            
