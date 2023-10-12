import pyglet

class FadeTransition:
    def __init__(self, window, duration=1.0):
        self.window = window
        self.duration = 1
        self.overlay = pyglet.shapes.Rectangle(0, 0, window.width, window.height, color=(0, 0, 0))
        self.opacity = 0
        self.is_fading = False

    def start_fade(self, fade_type="out"):
        self.is_fading = True
        if fade_type == "out":
            print("clock")
            pyglet.clock.schedule_interval(self.fade_out, 1/60.0)
        else:
            pyglet.clock.schedule_interval(self.fade_in, 1/60.0)

    def fade_out(self, dt):
        self.opacity += (255 / (self.duration * 60))
        if self.opacity >= 255:
            pyglet.clock.unschedule(self.fade_out)
            self.is_fading = False
        self.overlay.opacity = int(self.opacity)

    def fade_in(self, dt):
        self.opacity -= (255 / (self.duration * 60))
        if self.opacity <= 0:
            pyglet.clock.unschedule(self.fade_in)
            self.is_fading = False
        self.overlay.opacity = int(self.opacity)

    def draw(self):
        print("DRAWN")
        if self.is_fading:
            self.overlay.draw()