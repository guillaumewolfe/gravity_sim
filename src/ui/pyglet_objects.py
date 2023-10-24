import pyglet
from pyglet import shapes
from pyglet.gl import *
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

class Button:
    def __init__(self, window, x_rel, y_rel, width_rel, height_rel, text, color,font,opacity=255, enable = True,activated=True, isHighlight = False, highlight_color = (255,0,0,20),isOn=0,button_sound = "normal",id = None):
        self.window = window
        self.x_rel = x_rel
        self.y_rel = y_rel
        self.width_rel = width_rel
        self.height_rel = height_rel
        self.text = text
        if id:
            self.id = id
        else:
            self.id = text
        self.color = color
        self.rectangle = None
        self.label = self.text
        self.font=font
        self.hover = False
        self.opacity = opacity
        self.isActivated = activated
        
        #Sounds
        self.sounds = {}
        self.sounds["normal"] = pyglet.media.load('assets/sounds/normal_button.mp3', streaming=False)
        self.sounds["start"] = pyglet.media.load('assets/sounds/normal_button.mp3', streaming=False)
        self.sounds["menu"] = pyglet.media.load('assets/sounds/menu.mp3', streaming=False)
        self.sounds["close"] = pyglet.media.load('assets/sounds/close.mp3', streaming=False)
        self.sounds["hover"] = pyglet.media.load('assets/sounds/select.wav', streaming=False)
        self.sounds["warning"] = pyglet.media.load('assets/sounds/warning_click.wav', streaming=False)
        self.sounds["selectionPlanete"] = pyglet.media.load('assets/sounds/selection_planete.wav', streaming=False)
        self.sounds["addObject"] = pyglet.media.load('assets/sounds/open_creation.wav', streaming=False)
        self.sounds["removeObject"] = pyglet.media.load('assets/sounds/delete.wav', streaming=False)
        

        self.hoverSound = pyglet.media.load('assets/sounds/select.wav', streaming=False)
        self.ButtonSound = self.sounds[button_sound]

        self.click_color = (32, 247, 173, 255)
        self.padding_color = (255, 255,255 , 255)
        self.padding_color_perm = (255, 255,255 , 255)
        self.padding_color = (146, 230,211 , 255)
        self.padding_color_perm = (146, 230,211 , 255)

        #Highlight
        self.isHighligh = isHighlight
        self.highlight_color = highlight_color
        self.highlight_padding = 3

        self.isOn = isOn #0 = Pas activé, 1= On 2= Off
        self.OnColor = (76,230,107,50)
        self.OffColor = (255,0,0,50)

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

    def draw_highlight(self):
        if self.isOn == 1:
            color = self.OnColor
        elif self.isOn == 2:
            color = self.OffColor
        else:
            color = self.highlight_color
        rec = shapes.Rectangle(self.rectangle.x - self.highlight_padding, self.rectangle.y - self.highlight_padding, self.rectangle.width + 2 * self.highlight_padding, self.rectangle.height + 2 * self.highlight_padding, color=color[:3])
        rec.opacity = color[3]
        rec.draw()



    def draw(self):
        if not self.enabled: return
        if self.isHighligh:
            self.draw_highlight()
        if self.hover:
            if not self.hoverSoundPlayed:
                self.hoverSound.play()
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
        if not self.isActivated: return False
        return (self.rectangle.x < x < self.rectangle.x + self.rectangle.width and
                self.rectangle.y < y < self.rectangle.y + self.rectangle.height)

    def play_sound(self):
        self.ButtonSound.play()
    def click(self):
        if not self.enabled: return
        self.padding_color = self.click_color

    def unclick(self):
        if not self.enabled: return
        self.padding_color = self.padding_color_perm
    def change_sound(self,sound):
        self.ButtonSound = self.sounds[sound]


class Label:
    def __init__(self, size, text, x_percent, y_percent,font,color, font_size_percent=5,enable = True,x_anchor = "center",y_anchor="center"):
        self.window_width = size[0]
        self.window_height = size[1]
        self.text = text
        self.x_percent = x_percent
        self.y_percent = y_percent
        self.font_size_percent = font_size_percent
        self.color = color
        self.font=font
        self.enabled = enable or True
        self.x_anchor = x_anchor
        self.y_anchor = y_anchor
        
        self.label = pyglet.text.Label(
            self.text,
            font_name=font,
            font_size=self.calculate_font_size(),
            x=self.calculate_x(),
            y=self.calculate_y(),
            color=self.color,
            anchor_x=self.x_anchor, anchor_y=self.y_anchor
        )
    
    def calculate_x(self):
        return self.window_width * self.x_percent

    def calculate_y(self):
        return self.window_height * self.y_percent

    def calculate_font_size(self):
        return self.window_height * (self.font_size_percent / 100.0)

    def draw(self):
        if not self.enabled: return
        self.label.font_size = self.calculate_font_size()
        self.label.x = self.calculate_x()
        self.label.y = self.calculate_y()
        self.label.draw()

