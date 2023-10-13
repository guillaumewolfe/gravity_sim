import pyglet
from pyglet import shapes
from pyglet_objects import Button,Label
from pyglet.gl import *
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.engine import render
from src.engine import physics
from celestial_objects import CelestialObject,create_celestial_objects,CELESTIAL_PARAMETERS
from memory_profiler import profile
from transition import FadeTransition
from raycast import dot,intersect,get_normalized_coordinates,intersect_ray_sphere


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
        self.buttons=[]
        self.fade_duration = 1
        self.fade_transition = FadeTransition(self.window,duration = self.fade_duration)
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

    def load_shared_resources(self):
        global ressources
        if not ressources:
            ressources["background_video"] = pyglet.media.load('assets/animations/back.mp4')
            ressources["background_music"] = pyglet.media.load('assets/sounds/music_background.mp3',streaming=False)
        return ressources

    def transition_out(self):
        self.fade_transition.start_fade("out")
    def transition_in(self):
        self.fade_transition.start_fade("in")



    def switch_state(self,NewState):
        #self.transition_out()
        pyglet.clock.schedule_once(lambda dt:self.exit(),1)
        self.next_state=NewState(self.window)


    def exit(self):
        pass
    def close_app(self):
        pyglet.app.exit()
    def pause(self):
        pass

    def on_mouse_press(self,x,y,button,modifiers):
        pass













class StartMenuState(BaseState):
    videoPlayer = None
    musicPlayer = None

    def __init__(self,window):
        self.window = window
        super().__init__()
        self.medias = self.load_shared_resources()
        self.background_video = self.medias["background_video"]
        self.background_music = self.medias["background_music"]
        self.video_texture = None
        self.font="Open Sans"
        self.objects=[]



        self.createVideo()
        self.createMusic()

        self.label_welcome = Label(window, 'Bienvenue!', 0.5, 0.8,self.font,(255, 255, 255, 255),12)

        self.buttons = [
            Button(self.window, 0.5, 0.45, 0.25, 0.1, "Start", (255, 255, 255),self.font,opacity=175),
            Button(self.window, 0.5, 0.3, 0.25, 0.1, "Close", (255, 255,255),self.font,opacity=175)
        ]

    def enter(self):
        # Initialisez les éléments du menu
        pass
    def createVideo(self):
        if  StartMenuState.videoPlayer is None:
            StartMenuState.videoPlayer = pyglet.media.Player()
            StartMenuState.videoPlayer.queue(self.background_video)
            StartMenuState.videoPlayer.loop = True
            video_duration = StartMenuState.videoPlayer.source.duration
            StartMenuState.videoPlayer.seek(video_duration/2) 
            render.setup_2d_projection(self.window)  
        StartMenuState.videoPlayer.play()

        if not self.video_texture:
            self.video_texture = StartMenuState.videoPlayer.get_texture()
        self.window.set_visible(True)

    def createMusic(self):
        if StartMenuState.musicPlayer is None:
            StartMenuState.musicPlayer = pyglet.media.Player()
            StartMenuState.musicPlayer.queue(self.background_music)
            StartMenuState.musicPlayer.loop = True
            StartMenuState.musicPlayer.play()

    def update(self,dt):
        # Vérifiez si un bouton a été cliqué, etc.
        pass
    def update_positions(self):
        if self.video_texture:
            self.video_texture.blit(0,0)
        for button in self.buttons:
            button.update_position()

    def draw(self):
        # Update "Start" button position
        render.setup_2d_projection(self.window)
        self.update_positions()
        self.label_welcome.draw()
        for button in self.buttons:
            button.draw()

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
                    self.switch_state(SimulationState)
                elif btn.text == "Close":
                    btn.play_sound("close")
                    pyglet.clock.schedule_once(lambda dt:self.close_app(),0.8)
                    self.close_app()


    def exit(self):
        if StartMenuState.videoPlayer is not None:  
            StartMenuState.videoPlayer.pause()
















class SimulationState(BaseState):
    def __init__(self,window):
        self.window = window
        super().__init__()
        self.frame_buffer = render.FrameBuffer(*window.get_size())
        self.isPaused = False
        self.simulation_time = 0  # représente le temps écoulé en secondes (ou toute autre unité de temps que vous souhaitez utiliser)
        self.time_multiplier = 10_000
        self.time_multiplier = 1

        self.font="Open Sans"
        self.labels = [
            Label(window, 'Simulation', 0.5, 0.9,self.font,(255, 255, 255, 205),4),
            Label(window, f"Simulation Time: {self.simulation_time:.2f} seconds", 0.5, 0.1,self.font,(126, 161, 196, 255),2),
            Label(window, f"Time multiplier: x {self.time_multiplier:,}".replace(","," "), 0.5, 0.15,self.font,(126, 161, 196, 255),2)           
                       ]
        

        self.buttons = [
            Button(self.window, 0.125, 0.0925, 0.1875, 0.075, "Menu", (255, 255, 255),self.font,opacity=200),
            Button(self.window, 0.875, 0.0925, 0.1875, 0.055, "Restart", (255, 255, 255),self.font,opacity=200),
            Button(self.window, 0.5, 0.0325, 0.0875, 0.055, "Pause", (255, 255, 255),self.font,opacity=200),
            Button(self.window, 0.875, 0.1725, 0.1275, 0.055, "Reset Position", (255, 255, 255),self.font,opacity=200),
            ]
        self.objects = create_celestial_objects(CELESTIAL_PARAMETERS)
        background_image = pyglet.image.load("assets/textures/background.jpg")
        self.background_texture = background_image.get_texture()
    def enter(self):
        pass

    def update(self,dt):
        if not self.isPaused:
            self.simulation_time += dt * self.time_multiplier
            physics.update_physics(self.objects,dt* self.time_multiplier)
        self.labels[1] = Label(self.window, f"Simulation Time: {self.simulation_time/86400:.2f} jours", 0.5, 0.1, self.font, (126, 161, 196, 255), 2)
        self.labels[2] = Label(self.window, f"Time multiplier: x {self.time_multiplier:,}".replace(","," "), 0.5, 0.15,self.font,(126, 161, 196, 255),2)
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
    def restart(self):
        self.reset_positions()
        self.objects = None
        self.objects = create_celestial_objects(CELESTIAL_PARAMETERS)
        self.time_multiplier = 1
        self.simulation_time=0


    def draw(self):
        render.draw_objects(self.window,self.labels,self.buttons, self.objects,self.rotation_x,self.rotation_y,self.rotation_z,self.translation_x,self.translation_y,self.zoom,self.background_texture)

    def on_mouse_press(self, x, y, button, modifiers):
        render.draw_objects(self.window,self.labels,self.buttons, self.objects,self.rotation_x,self.rotation_y,self.rotation_z,self.translation_x,self.translation_y,self.zoom,self.background_texture,selection_mode=True,frame_buffer=self.frame_buffer)
        pixel_data = (GLubyte*3)()
        glReadPixels(x,y,1,1,GL_RGB,GL_UNSIGNED_BYTE, pixel_data)
        pixel_color = [pixel_data[i]/255.0 for i in range(3)]
        selected_object_index = int(pixel_color[0]*255)
        selected_object = self.objects[selected_object_index]
        print(f"Selected object: {selected_object.name}")
        glBindFramebuffer(GL_FRAMEBUFFER_EXT,0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)



        for btn in self.buttons:
            btn.click()



    def modify_time_modifier(self,scroll_y):
        sensibility = 10_000
        self.time_multiplier += scroll_y*sensibility
        if self.time_multiplier == 0:
            self.time_multiplier=1
        if self.time_multiplier!=1:
            if self.time_multiplier%10!=0:
                self.time_multiplier -= 1

    
    def pause(self):
        for btn in self.buttons:
            if btn.text == "Pause":
                btn.text = "Resume"
                btn.play_sound("normal")
            elif btn.text == "Resume":
                btn.text = "Pause"
                btn.play_sound("normal")
                
        if self.isPaused:
            self.isPaused=False
        else:
            self.isPaused=True

        
    def on_mouse_released(self, x, y, button, modifiers):
        for btn in self.buttons:
            btn.unclick()
            if btn.contains_point(x, y):
                    
                    if btn.text == "Menu":
                        btn.play_sound("menu")
                        self.switch_state(StartMenuState)
                        
                    if btn.text == "Restart":
                        btn.play_sound("normal")
                        self.restart()

                    if btn.text == "Pause" or btn.text == "Resume":
                        self.pause()
                    
                    if btn.text == "Reset Position":
                        btn.play_sound("normal")
                        self.reset_positions()




class LoadingState(BaseState):
    def __init__(self,window):
        self.window = window
        super().__init__()
        self.medias = {}

        self.loading_video = pyglet.media.load('assets/animations/loading_dust.mp4')
        self.labels = Label(window, 'Chargement...', 0.5, 0.1,"Open Sans",(255, 255, 255, 210),3)
        self.loading_animation = False
        self.loadingTime = 0
        self.window.flip()
        if self.loading_animation:
            self.loadingTime = 2
            self.initiate_loading_animation()
        self.load_media()
        pyglet.clock.schedule_once(self.switch_to_menu,self.loadingTime)


    
    def load_media(self):
        self.medias["background_video"] = pyglet.media.load('assets/animations/back.mp4')
        self.medias["background_music"] = pyglet.media.load('assets/sounds/music_background.mp3',streaming=False)
        global ressources
        ressources = self.medias

    def initiate_loading_animation(self):
        self.videoPlayer = pyglet.media.Player()
        self.videoPlayer.queue(self.loading_video)
        self.videoPlayer.loop = True

        render.setup_2d_projection(self.window)
        self.videoPlayer.play()
    
    def draw(self):
        if self.loading_animation:
            texture = self.videoPlayer.get_texture()
            if texture:
                texture.blit(0,0)
        self.labels.draw()

    
    def switch_to_menu(self,dt=None):
        self.switch_state(StartMenuState)
    
    def exit(self):
        if self.loading_animation:
            print("exit")
            self.videoPlayer.pause()
            self.videoPlayer.delete()









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
