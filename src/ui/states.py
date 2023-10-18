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
        pyglet.font.add_file("assets/fonts/TiltNeon-Regular.ttf")
        self.font="Tilt Neon"
    def enter(self):
        pass
    def on_mouse_released(self,x,y,pressed,modif,isAjusting = False):
        pass

    def update(self,dt):
        pass
    def draw(self):
        pass
    def rotation(self, dx, dy,dz):
        # Mettez à jour les angles de rotation en fonction du mouvement de la souris
        sensitivity = 0.5
        self.rotation_x += dy * sensitivity
        self.rotation_y += dx * sensitivity   
        self.rotation_z += dz * sensitivity   
    def translation(self, dx, dy):
        # Mettez à jour les angles de rotation en fonction du mouvement de la souris
        sensitivity = 0.05
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
    def modify_time_modifier(self):
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
        self.objects=[]



        self.createVideo()
        self.createMusic()

        self.labels = [
            Label(window, 'Space Query', 0.5, 0.8,self.font,(255, 255, 255, 255),12),
            Label(window, 'Main Menu', 0.5, 0.25,self.font,(255, 255, 255, 255),3),
        ]

        self.buttons = [
            Button(self.window, 0.5, 0.20, 0.15, 0.05, "Start", (255, 255, 255),self.font,opacity=50,button_sound="start"),
            Button(self.window, 0.5, 0.14, 0.15, 0.05, "Options", (255, 255, 255),self.font,opacity=50,button_sound="normal"),
            Button(self.window, 0.5, 0.08, 0.15, 0.05, "Close", (255, 255,255),self.font,opacity=50,button_sound="close")
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
            self.setup_2d_projection()  
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


    def setup_2d_projection(self):
        glDisable(GL_DEPTH_TEST)
        glViewport(0, 0, self.window.width, self.window.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.window.width, 0, self.window.height)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()


    def update_positions(self):
        if self.video_texture:
            self.video_texture.blit(0,0,width=self.window.width,height=self.window.height)
        for btn in self.buttons:
            btn.update_position()


    def draw(self):
        # Update "Start" button position
        self.setup_2d_projection()
        self.update_positions()
        for label in self.labels:
            label.draw()
        for button in self.buttons:
            button.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        for btn in self.buttons:
            btn.click()
    def on_mouse_released(self, x, y, button, modifiers,isAjusting):
        for btn in self.buttons:
            btn.unclick()
            if btn.contains_point(x, y):
                if btn.text == "Start":
                    btn.play_sound()
                    self.draw()
                    self.switch_state(SimulationState)
                elif btn.text == "Close":
                    btn.play_sound()
                    pyglet.clock.schedule_once(lambda dt:self.close_app(),0.8)
                    self.close_app()


    def exit(self):
        if StartMenuState.videoPlayer is not None:  
            StartMenuState.videoPlayer.pause()
















class SimulationState(BaseState):
    def __init__(self,window):
        self.window = window
        super().__init__()
        self.medias = self.load_shared_resources()
        self.frame_buffer = render.FrameBuffer(*window.get_size())
        self.isPaused = False
        self.simulation_time = 0  # représente le temps écoulé en secondes (ou toute autre unité de temps que vous souhaitez utiliser)
        self.time_multiplier = 10_000
        self.time_multiplier = 1
        self.selected_object = None
        self.couleur_label = (255,255,255,200)
        self.labels = [
            Label(window, 'Simulation', 0.5, 0.9,self.font,(255, 255, 255, 0),4),
            Label(window, f"Simulation Time: {self.simulation_time:.2f} seconds", 0.5, 0.0325,self.font,self.couleur_label,2),
            Label(window, f"Time multiplier: x {self.time_multiplier:,}".replace(","," "), 0.5, 0.0825,self.font,self.couleur_label,2),  
            Label(self.window, f"Selected object : ", 0.5, 0.1325,self.font,self.couleur_label,2)         
                       ]
        
        diff = 0.055
        restart_pos = 0.0425
        reset_pos = restart_pos+diff
        menu_pos = restart_pos+2*diff
        pause_pos = restart_pos+3*diff
        axes_pos = restart_pos+4*diff

        self.buttons = [
            Button(self.window, 0.900, menu_pos, 0.1175, 0.045, "Menu", (255, 255, 255),self.font,opacity=20,button_sound="menu"),
            Button(self.window, 0.900, restart_pos, 0.1175, 0.045, "Restart", (255, 255, 255),self.font,opacity=20,button_sound="normal"),
            Button(self.window, 0.9, pause_pos, 0.1175, 0.045, "Pause", (255, 255, 255),self.font,opacity=20,button_sound="normal"),
            Button(self.window, 0.900, reset_pos, 0.1175, 0.045, "Reset Position", (255, 255, 255),self.font,opacity=20,button_sound="normal"),
            Button(self.window, 0.375, 0.1325, 0.0675, 0.040, "Zoom", (255, 255, 255),self.font,opacity=20,enable=False,button_sound="normal"),
            Button(self.window, 0.900, axes_pos, 0.1175, 0.045, "Axes", (255, 255, 255),self.font,opacity=20,isHighlight=True,isOn=2,button_sound="normal"),
            ]
        self.objects = create_celestial_objects(CELESTIAL_PARAMETERS)
        background_image = pyglet.image.load("assets/textures/background.jpg")
        self.background_texture = background_image.get_texture()
        self.renderTool = render.RenderTool(window,self.labels,self.buttons,self.objects,self.rotation_x,self.rotation_y,self.rotation_z,self.translation_x,self.translation_y,self.zoom,self.background_texture)
        self.renderTool.maxlength = self.max_length()
    def max_length(self):
        maxd = 0
        for obj in self.objects:
            distance = (obj.position_simulation[0]**2+obj.position_simulation[1]**2+obj.position_simulation[0]**2)**0.5
            if distance > maxd:
                maxd = distance
        return maxd
    def enter(self):
        pass

    def update(self,dt):
        if self.selected_object:
            text = self.selected_object.name
        else:
            text = "None"
        if not self.isPaused:
            self.simulation_time += dt * self.time_multiplier
            physics.update_physics(self.objects,dt* self.time_multiplier)
        self.labels[1] = Label(self.window, f"Simulation Time: {self.simulation_time/86400:.2f} jours", 0.5, 0.0325, self.font, self.couleur_label, 2)
        self.labels[2] = Label(self.window, f"Time multiplier: x {self.time_multiplier:,}".replace(","," "), 0.5, 0.0825,self.font,self.couleur_label,2)
        self.labels[3] = Label(self.window, f"Selected object: {text}", 0.5, 0.1325,self.font,self.couleur_label,2)
    def reset_positions(self):
        self.rotation_x = 0 
        self.rotation_y = 0 
        self.rotation_z = 0 
        self.translation_x = 0
        self.translation_y = 0
        self.zoom = 0
        self.renderTool.followObjectEnabled = False
    def restart(self):
        self.reset_positions()
        self.objects = None
        self.objects = create_celestial_objects(CELESTIAL_PARAMETERS)
        self.time_multiplier = 1
        self.simulation_time=0
        self.selected_object = None
        

    def update_render_tool(self):
        self.renderTool.update(self.labels,self.buttons,self.objects,self.rotation_x,self.rotation_y,self.rotation_z,self.translation_x,self.translation_y,self.zoom)
        self.renderTool.selectedObject = self.selected_object
    def draw(self):
        #On update les valeurs
        self.update_render_tool()
        #On dessine
        self.renderTool.draw()

    def check_selection(self,x,y):
        self.update_render_tool()
        self.selected_object = self.renderTool.selection_mode(x,y)
        if self.selected_object is not None:
            self.medias["bruit_selection_planete"].play()
            self.buttons[4].enabled = True
        else :
            self.buttons[4].enabled = False



    def on_mouse_press(self, x, y, button, modifiers):
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
                btn.play_sound()
            elif btn.text == "Resume":
                btn.text = "Pause"
                btn.play_sound()
                
        if self.isPaused:
            self.isPaused=False
        else:
            self.isPaused=True

        
    def on_mouse_released(self, x, y, button, modifiers,isAjusting):
        buttonClicked = False

        for btn in self.buttons:
            btn.unclick()
            if btn.contains_point(x, y):
                buttonClicked = True
                if btn.text == "Menu":
                    btn.play_sound()
                    self.switch_state(StartMenuState)

                    
                if btn.text == "Restart":
                    btn.play_sound()
                    self.restart()


                if btn.text == "Pause" or btn.text == "Resume":
                    self.pause()

                
                if btn.text == "Reset Position":
                    btn.play_sound()
                    self.reset_positions()
                

                if btn.text == "Zoom":
                    self.reset_positions()
                    self.renderTool.followObjectEnabled = True
                    self.renderTool.followObject = self.renderTool.selectedObject

                if btn.text == "Axes":
                    if self.renderTool.axesEnable:
                        self.renderTool.axesEnable = False
                        btn.isOn = 2
                    else:
                        self.renderTool.axesEnable = True
                        btn.isOn = 1
                    btn.play_sound()



        if not buttonClicked and not isAjusting:
            self.check_selection(x,y)
                        


            




class LoadingState(BaseState):
    def __init__(self,window):
        self.window = window
        super().__init__()
        self.medias = {}
        self.loading_animation = False
        self.loadingTime = 0
        self.load_media()
        self.switch_to_menu()


    
    def load_media(self):
        self.medias["background_video"] = pyglet.media.load('assets/animations/back.mp4')
        self.medias["background_video"] = pyglet.media.load('assets/animations/intro4.mp4')
        self.medias["background_music"] = pyglet.media.load('assets/sounds/music_background.mp3',streaming=False)
        self.medias["bruit_selection_planete"] = pyglet.media.load('assets/sounds/selection_planete.wav', streaming=False)
        global ressources
        ressources = self.medias

    
    def switch_to_menu(self,dt=None):
        self.switch_state(StartMenuState)
    
    def exit(self):
        if self.loading_animation:
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
