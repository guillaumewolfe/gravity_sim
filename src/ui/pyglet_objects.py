import pyglet
from pyglet import shapes

class Button:
    def __init__(self, window, x_rel, y_rel, width_rel, height_rel, text, color,font):
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
        self.padding_color = (32, 247, 173, 255)
        self.padding_color = (255, 255,255 , 255)
        self.hover_padding = 5  # La taille supplémentaire pour l'effet de surbrillance
        self.rectangle = shapes.Rectangle(0, 0, 0, 0, color=self.color)
        self.label = pyglet.text.Label('', font_name=self.font, font_size=12,
                                       x=0, y=0, anchor_x='center', anchor_y='center')
        self.hover_rectangle = shapes.Rectangle(0, 0, 0, 0, color=self.padding_color[:3])
        
        # Appelez update_position pour initialiser leurs positions
        self.update_position()

    def update_position(self):
        width = self.window.width * self.width_rel
        height = self.window.height * self.height_rel
        x = self.window.width * self.x_rel - width // 2
        y = self.window.height * self.y_rel - height // 2
        
        self.rectangle.x = x
        self.rectangle.y = y
        self.rectangle.width = width
        self.rectangle.height = height
        
        self.label.text = self.text
        self.label.font_size = height * 0.4
        self.label.x = self.window.width * self.x_rel
        self.label.y = self.window.height * self.y_rel

        self.hover_rectangle.x = x - self.hover_padding
        self.hover_rectangle.y = y - self.hover_padding
        self.hover_rectangle.width = width + 2 * self.hover_padding
        self.hover_rectangle.height = height + 2 * self.hover_padding
    def draw(self):
        if self.hover:
            color = self.padding_color
            self.hover_rectangle.draw()
        else:
            color = (126, 161, 196, 255) 
        self.label.color = color
        self.rectangle.draw()
        self.label.draw()
    def contains_point(self, x, y):
        return (self.rectangle.x < x < self.rectangle.x + self.rectangle.width and
                self.rectangle.y < y < self.rectangle.y + self.rectangle.height)


class Label:
    def __init__(self, window, text, x_percent, y_percent,font,color, font_size_percent=5):
        self.window = window
        self.text = text
        self.x_percent = x_percent
        self.y_percent = y_percent
        self.font_size_percent = font_size_percent
        self.color = color
        self.font=font
        
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
        self.label.font_size = self.calculate_font_size()
        self.label.x = self.calculate_x()
        self.label.y = self.calculate_y()
        self.label.draw()