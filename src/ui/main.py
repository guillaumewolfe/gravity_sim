import pyglet
from pyglet import shapes,font
import controls
from pyglet.gl import *
import states


#Génération de la fenêtre
font.add_file('assets/fonts/OpenSans-VariableFont_wdth,wght.ttf')
myFont = "Open Sans"
#myFont = "Arial"
screen = pyglet.canvas.get_display().get_default_screen()
WIDTH, HEIGHT = 1000,800
window = pyglet.window.Window(WIDTH, HEIGHT, "Start Menu", resizable=True)
window.set_location((screen.width - WIDTH) // 2, (screen.height - HEIGHT) // 2)
glClearColor(6/255, 20/255, 38/255, 1)


@window.event
def on_draw():
    window.clear()
    current_state.draw()

def update(dt):
    global current_state
    current_state.update()

    if current_state.next_state:
        current_state = current_state.next_state
        controls.handle_input(window, current_state)

pyglet.clock.schedule_interval(update, 1/30.0)


#FPS:
#Boucle
def main():
    global current_state
    current_state = states.StartMenuState(window)
    controls.handle_input(window, current_state)
    pyglet.app.run()


if __name__ == "__main__":
    main()