import pyglet
from pyglet import shapes
from pyglet.gl import *
import states

isShiftPressed = False
isMousePressed = False
isAjusting = False

def handle_input(window, current_state):
    @window.event
    def on_mouse_press(x, y, button, modifiers):
        global isMousePressed
        isMousePressed = True
        current_state.on_mouse_press(x, y, button, modifiers)



    @window.event
    def on_mouse_release(x, y, button, modifiers):
        global isMousePressed
        isMousePressed = False
        global isAjusting
        current_state.on_mouse_released(x, y, button, modifiers,isAjusting)
        isAjusting = False
        if hasattr(current_state, 'isCreating'):
            if current_state.isCreating:
                current_state.OutilCreation.on_mouse_release(x,y)
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
        if hasattr(current_state, 'isCreating'):
            if current_state.isCreating:
                current_state.OutilCreation.on_mouse_motion(x,y)
        for btn in current_state.buttons:
            if btn.contains_point(x, y):
                btn.hover = True
            else:
                btn.hover = False



    @window.event
    def on_mouse_drag(x, y, dx, dy, button, modifiers):

        global isAjusting 
        isAjusting = True
        if button == pyglet.window.mouse.RIGHT:
            current_state.rotation(dx, dy, 0)
        if button == pyglet.window.mouse.LEFT:
            current_state.translation(dy, dx) 

    @window.event
    def on_mouse_scroll(x, y, scroll_x, scroll_y):

        global isShiftPressed
        global isMousePressed
        if isShiftPressed:
            current_state.modify_time_modifier(scroll_y) 
        else:
            current_state.zoomer(scroll_y) 


    @window.event
    def on_key_press(symbol, modifier):
        if symbol == pyglet.window.key.UP:
            current_state.modify_time_modifier(1) 
        if symbol == pyglet.window.key.DOWN:
            current_state.modify_time_modifier(-1)
        if symbol == pyglet.window.key.SPACE:
            current_state.pause()




        if hasattr(current_state, 'isCreating'):
            if current_state.isCreating:
                if symbol == pyglet.window.key.Q:
                    current_state.OutilCreation.on_key_press(symbol)
                if symbol == pyglet.window.key.E:
                    current_state.OutilCreation.on_key_press(symbol)

        




        if symbol == pyglet.window.key.LSHIFT or symbol == pyglet.window.key.RSHIFT:
            global isShiftPressed
            isShiftPressed = True

    @window.event
    def on_key_release(symbol, modifier):
        if symbol == pyglet.window.key.LSHIFT or symbol == pyglet.window.key.RSHIFT:
            global isShiftPressed
            isShiftPressed = False

        
                
