import pyglet
from pyglet import shapes
from pyglet_objects import Button,Label
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.engine import render
from src.engine import physics
from celestial_objects import CelestialObject,create_celestial_objects,CELESTIAL_PARAMETERS
from threading import Thread

ressources = {}





class BaseState:
    def __init__(self):
        self.next_state = None
        self.rotation_x = 0
        self.rotation_y = 0
        self.rotation_z = 0
        self.translation_y = 0
        self.translation_x = 0
        self.zoom = 0
    def enter(self):
        pass
    def on_mouse_released(self,x,y,pressed,modif):
        pass

    def update(self,dt):
        pass
    def rotation(self, dx, dy,dz):
        # Mettez à jour les angles de rotation en fonction du mouvement de la souris
        sensitivity = 0.5
        self.rotation_x += dy * sensitivity
        self.rotation_y += dx * sensitivity   
        self.rotation_z += dz * sensitivity   
    def translation(self, dx, dy):
        # Mettez à jour les angles de rotation en fonction du mouvement de la souris
        sensitivity = 0.01
        self.translation_x += dy * sensitivity
        self.translation_y += dx * sensitivity  
    def zoomer(self, zoom):
        # Mettez à jour les angles de rotation en fonction du mouvement de la souris
        sensitivity = 1
        self.zoom += zoom * sensitivity
    def exit(self):
        pass
    def close_app(self):

        pyglet.app.exit()













class StartMenuState(BaseState):
    def __init__(self,window):
        super().__init__()
        self.window = window
        global ressources
        medias = ressources
        self.background_video = medias["background_video"]
        self.background_music = medias["background_music"]
        self.background_sprite = medias["background_sprite"]
        self.font="Open Sans"

        self.createVideoAndSound()

        self.label_welcome = Label(window, 'Bienvenue!', 0.5, 0.8,self.font,(255, 255, 255, 255),12)


        self.buttons = [
            Button(self.window, 0.5, 0.45, 0.25, 0.1, "Start", (255, 255, 255),self.font,opacity=175),
            Button(self.window, 0.5, 0.3, 0.25, 0.1, "Close", (255, 255,255),self.font,opacity=175)
        ]

    def on_mouse_press(self, x, y, button, modifiers):
            for btn in self.buttons:
                btn.click()
    def on_mouse_released(self, x, y, button, modifiers):
        for btn in self.buttons:
            btn.unclick()
            if btn.contains_point(x, y):
                if btn.text == "Start":
                    btn.play_sound("start")
                    self.draw()
                    self.next_state = SimulationState(self.window)
                elif btn.text == "Close":
                    btn.play_sound("close")
                    pyglet.clock.schedule_once(lambda dt:self.close_app(),0.8)
                    #self.close_app()

    def enter(self):
        # Initialisez les éléments du menu
        pass
    def createVideoAndSound(self):
        self.videoPlayer = pyglet.media.Player()
        self.videoPlayer.queue(self.background_video)
        self.videoPlayer.loop = True

        render.setup_2d_projection(self.window)
        self.videoPlayer.play()

        self.background_music.loop = True
        self.background_music.play()


    def update(self,dt):
        # Vérifiez si un bouton a été cliqué, etc.
        #update_physics()
        pass
    def update_positions(self):
        self.videoPlayer.get_texture().blit(0,0)
        for button in self.buttons:
            button.update_position()


    def draw(self):
        # Update "Start" button position
        render.setup_2d_projection(self.window)
        self.update_positions()
        self.label_welcome.draw()
        for button in self.buttons:
            button.draw()

















class SimulationState(BaseState):
    def __init__(self,window):
        super().__init__()

        self.simulation_time = 0  # représente le temps écoulé en secondes (ou toute autre unité de temps que vous souhaitez utiliser)
        self.time_multiplier = 2

        self.font="Open Sans"
        self.window = window
        self.labels = [
            Label(window, 'Simulation', 0.5, 0.9,self.font,(255, 255, 255, 205),4),
            Label(window, f"Simulation Time: {self.simulation_time:.2f} seconds", 0.5, 0.1,self.font,(126, 161, 196, 255),2)           
                       ]
        

        self.buttons = [
            Button(self.window, 0.125, 0.0925, 0.1875, 0.075, "Menu", (75, 87, 102),self.font),
            Button(self.window, 0.875, 0.0925, 0.1875, 0.055, "Reset Position", (75, 87, 102),self.font),
            ]
        self.objects = create_celestial_objects(CELESTIAL_PARAMETERS)
        background_image = pyglet.image.load("assets/textures/background.jpg")
        self.background_texture = background_image.get_texture()
    def enter(self):
        pass

    def update(self,dt):
       self.simulation_time += dt * self.time_multiplier
       self.labels[1] = Label(self.window, f"Simulation Time: {self.simulation_time:.2f} seconds", 0.5, 0.1, self.font, (126, 161, 196, 255), 2)
       physics.update_physics(self.objects,dt* self.time_multiplier)
    def update_positions(self):
        for button in self.buttons:
            button.update_position()
    def reset_positions(self):
        self.rotation_x = 0 
        self.rotation_y = 0 
        self.rotation_z = 0 
        self.translation_x = 0
        self.translation_y = 0
        self.zoom = 0
    def draw(self):
        render.draw_objects(self.window,self.labels,self.buttons, self.objects,self.rotation_x,self.rotation_y,self.rotation_z,self.translation_x,self.translation_y,self.zoom,self.background_texture)
    def on_mouse_press(self, x, y, button, modifiers):
        for btn in self.buttons:
            btn.click()
    def on_mouse_released(self, x, y, button, modifiers):
        for btn in self.buttons:
            btn.unclick()
            if btn.contains_point(x, y):
                    if btn.text == "Menu":
                        btn.play_sound("menu")
                        self.next_state = StartMenuState(self.window)
                        
                    if btn.text == "Reset Position":
                        btn.play_sound("normal")
                        self.reset_positions()

                        







class LoadingState(BaseState):
    def __init__(self,window):
        super().__init__()
        self.window = window
        self.medias = {}
        self.loading_video = pyglet.media.load('assets/animations/loading.mp4')
        self.labels = Label(window, 'Bienvenue!', 0.5, 0.8,"Arial",(255, 255, 255, 255),12)
        self.initiate_loading_animation()
        self.draw()
        self.window.flip()
        print("Here")

        self.load_thread = Thread(target=self.load_media())
        self.load_thread.start()

    
    def load_media(self):
        self.medias["background_video"] = pyglet.media.load('assets/animations/back.mp4')
        self.medias["background_music"] = pyglet.media.load('assets/sounds/music_background.mp3',streaming=False)
        self.medias["background_sprite"] = pyglet.sprite.Sprite(pyglet.image.load_animation('assets/gif/blue2.gif'))
        global ressources
        ressources = self.medias
        self.switch_to_menu()

    def initiate_loading_animation(self):
        self.videoPlayer = pyglet.media.Player()
        self.videoPlayer.queue(self.loading_video)
        self.videoPlayer.loop = True

        render.setup_2d_projection(self.window)
        self.videoPlayer.play()
    
    def draw(self):
        self.labels.draw()
        print("called")
        self.videoPlayer.get_texture().blit(0,0)
    
    def switch_to_menu(self):
        self.next_state = StartMenuState(self.window)









class SettingsMenuState(BaseState):
    def enter(self):
        # Initialiser les éléments du menu de paramètres
        pass

    def update(self,dt):
        # Vérifier les modifications des paramètres
        pass

    def draw(self):
        # Dessiner le menu de paramètres
        pass
