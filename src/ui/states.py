import pyglet
from pyglet import shapes
from pyglet_objects import Button,Label

exit_condition = False
class BaseState:
    def __init__(self):
        self.next_state = None
    def enter(self):
        pass

    def update(self):
        pass

    def exit(self):
        pass
    def close_app(self):
        pyglet.app.exit()

class StartMenuState(BaseState):
    def __init__(self,window):
        super().__init__()
        self.window = window
        self.font="Open Sans"
        self.label_welcome = Label(window, 'Bienvenue!', 0.5, 0.7,self.font,(126, 161, 196, 255),12)
        self.buttons = [
            Button(self.window, 0.5, 0.45, 0.25, 0.1, "Start", (75, 87, 102),self.font),
            Button(self.window, 0.5, 0.3, 0.25, 0.1, "Close", (145, 89, 83),self.font)
        ]
    def on_mouse_press(self, x, y, button, modifiers):
            for btn in self.buttons:
                if btn.contains_point(x, y):
                    if btn.text == "Start":
                        self.next_state = SimulationState(self.window)
                        print("Bouton Start cliqué!")
                    elif btn.text == "Close":
                        self.close_app()
    def enter(self):
        # Initialisez les éléments du menu
        pass

    def update(self):
        # Vérifiez si un bouton a été cliqué, etc.
        pass
    def update_positions(self):
        for button in self.buttons:
            button.update_position()


    def draw(self):
        # Update "Start" button position
        self.update_positions()
        self.label_welcome.draw()
        for button in self.buttons:
            button.draw()

class SimulationState(BaseState):
    def __init__(self,window):
        super().__init__()
        self.font="Open Sans"
        self.window = window
        self.label_welcome = Label(window, 'Simulation!', 0.5, 0.7,self.font,(126, 161, 196, 255),5)
        self.buttons = [
            Button(self.window, 0.5, 0.45, 0.25, 0.1, "Menu", (75, 87, 102),self.font)]
    def enter(self):
        # Initialisation de la simulation
        pass
    def update(self):
        # Mise à jour de la simulation
        pass
    def update_positions(self):
        for button in self.buttons:
            button.update_position()
    def draw(self):
        # Rendu de la simulation
        self.label_welcome.draw()
        self.update_positions()
        for button in self.buttons:
            button.draw()
    def on_mouse_press(self, x, y, button, modifiers):
        for btn in self.buttons:
            if btn.contains_point(x, y):
                    if btn.text == "Menu":
                        self.next_state = StartMenuState(self.window)


class SettingsMenuState(BaseState):
    def enter(self):
        # Initialiser les éléments du menu de paramètres
        pass

    def update(self):
        # Vérifier les modifications des paramètres
        pass

    def draw(self):
        # Dessiner le menu de paramètres
        pass