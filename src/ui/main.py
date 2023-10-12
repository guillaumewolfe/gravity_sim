import pyglet
from pyglet import shapes,font
from pyglet.gl import *
import os
import sys
sys.path.insert(0, 'C:/Users/guill/Documents/gravity_sim/src/engine')
import controls
import states
import gc

#Génération de la fenêtre
font.add_file('assets/fonts/OpenSans-VariableFont_wdth,wght.ttf')
myFont = "Open Sans"
#myFont = "Arial"
screen = pyglet.canvas.get_display().get_default_screen()
WIDTH, HEIGHT = 1820,980
pyglet.options['vsync'] = False
window = pyglet.window.Window(WIDTH, HEIGHT, "Simulation", resizable=True)
window.set_location((screen.width - WIDTH) // 2, (screen.height - HEIGHT) // 2)
glClearColor(1,1,1, 1)
glEnable(GL_DEPTH_TEST)

@window.event
def on_draw():
    window.clear()
    current_state.draw()
    gc.collect()

def update(dt):
    global current_state
    current_state.update(dt)

    if current_state.next_state:
        current_state = current_state.next_state
        controls.handle_input(window, current_state)

pyglet.clock.schedule_interval(update, 1/30.0)



#FPS:
#Boucle
def main():
    global current_state
    current_state = states.LoadingState(window)
    controls.handle_input(window, current_state)
    pyglet.app.run()


if __name__ == "__main__":
    main()