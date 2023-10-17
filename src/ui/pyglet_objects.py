import pyglet
from pyglet import shapes
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

class Button:
    def __init__(self, window, x_rel, y_rel, width_rel, height_rel, text, color,font,opacity=255, enable = True):
        self.window = window
        self.x_rel = x_rel
        self.y_rel = y_rel
        self.width_rel = width_rel
        self.height_rel = height_rel
        self.text = text
        self.color = color
        self.rectangle = None
        self.label = None
        self.font=font
        self.hover = False
        self.opacity = opacity
        self.normalSound =  pyglet.media.load('assets/sounds/normal_button.mp3', streaming=False)
        self.startSound = pyglet.media.load('assets/sounds/start.mp3', streaming=False)
        self.menuSound = pyglet.media.load('assets/sounds/menu.mp3', streaming=False)
        self.closeSound = pyglet.media.load('assets/sounds/close.mp3', streaming=False)
        self.hoverSound = pyglet.media.load('assets/sounds/select.wav', streaming=False)
        self.warningSound = pyglet.media.load('assets/sounds/warning_click.wav', streaming=False)
        self.selectionPlaneteSound = pyglet.media.load('assets/sounds/selection_planete.wav', streaming=False)
        self.click_color = (32, 247, 173, 255)
        self.padding_color = (255, 255,255 , 255)
        self.padding_color_perm = (255, 255,255 , 255)
        self.padding_color = (146, 230,211 , 255)
        self.padding_color_perm = (146, 230,211 , 255)
        #self.padding_color = (140, 158, 189, 255)
        #self.padding_color_perm = (140, 158, 189, 255)
        self.hover_padding = 3  # La taille supplémentaire pour l'effet de surbrillance
        self.rectangle = shapes.Rectangle(0, 0, 0, 0, color=self.color)
        self.rectangle.opacity = opacity
        self.label = pyglet.text.Label('', font_name=self.font, font_size=12,
                                       x=0, y=0, anchor_x='center', anchor_y='center')
        self.hover_rectangle = shapes.Rectangle(0, 0, 0, 0, color=self.padding_color[:3])
        self.hover_rectangle.opacity=opacity
        self.enabled = enable 
        self.hoverSoundPlayed = False
        
        # Appelez update_position pour initialiser leurs positions
        self.update_position()


    def update_position(self):
        if not self.enabled: return
        width = self.window.width * self.width_rel
        height = self.window.height * self.height_rel
        x = self.window.width * self.x_rel - width // 2
        y = self.window.height * self.y_rel - height // 2
        
        self.rectangle.x = x
        self.rectangle.y = y
        self.rectangle.width = width
        self.rectangle.height = height
        
        self.label.text = self.text
        self.label.font_size = height * 0.35
        self.label.x = self.window.width * self.x_rel
        self.label.y = self.window.height * self.y_rel

        self.hover_rectangle.x = x - self.hover_padding
        self.hover_rectangle.y = y - self.hover_padding
        self.hover_rectangle.width = width + 2 * self.hover_padding
        self.hover_rectangle.height = height + 2 * self.hover_padding

    def draw(self):
        if not self.enabled: return
        if self.hover:
            if not self.hoverSoundPlayed:
                self.play_sound("hover")
                self.hoverSoundPlayed = True
            color = self.padding_color
            self.hover_rectangle.color=self.padding_color[:3]
            self.hover_rectangle.draw()
        else:
            self.hoverSoundPlayed = False
            color = (140, 158, 189, 255) 
            color = (255, 255, 255, 255) 
        self.label.color = color
        self.rectangle.draw()
        self.label.draw()
    def contains_point(self, x, y):
        if not self.enabled: return False
        return (self.rectangle.x < x < self.rectangle.x + self.rectangle.width and
                self.rectangle.y < y < self.rectangle.y + self.rectangle.height)

    def play_sound(self,soundType):
        if soundType == "normal":
            self.normalSound.play()
        elif soundType == "menu":
            self.menuSound.play()
        elif soundType == "start":
            self.startSound.play()
        elif soundType == "close":
            self.closeSound.play()
        elif soundType == "hover":
            self.hoverSound.play()
    def click(self):
        if not self.enabled: return
        self.padding_color = self.click_color

    def unclick(self):
        if not self.enabled: return
        self.padding_color = self.padding_color_perm

class Label:
    def __init__(self, window, text, x_percent, y_percent,font,color, font_size_percent=5,enable = True):
        self.window = window
        self.text = text
        self.x_percent = x_percent
        self.y_percent = y_percent
        self.font_size_percent = font_size_percent
        self.color = color
        self.font=font
        self.enabled = enable or True
        
        self.label = pyglet.text.Label(
            self.text,
            font_name=font,
            font_size=self.calculate_font_size(),
            x=self.calculate_x(),
            y=self.calculate_y(),
            color=self.color,
            anchor_x='center', anchor_y='center'
        )
    
    def calculate_x(self):
        return self.window.width * self.x_percent

    def calculate_y(self):
        return self.window.height * self.y_percent

    def calculate_font_size(self):
        return self.window.height * (self.font_size_percent / 100.0)

    def draw(self):
        if not self.enabled: return
        self.label.font_size = self.calculate_font_size()
        self.label.x = self.calculate_x()
        self.label.y = self.calculate_y()
        self.label.draw()

