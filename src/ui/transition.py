import pyglet

class FadeTransition:
    opacity = 0
    def __init__(self, window, duration=1.0):
        self.window = window
        self.duration = duration
        self.overlay = pyglet.shapes.Rectangle(0, 0, window.width, window.height, color=(0, 0, 0))
        self.is_fading = False

    def start_fade(self, fade_type="out"):
        print(f"Starting fade :{fade_type}")
        self.is_fading = True
        if fade_type == "out":
            pyglet.clock.schedule_interval(self.fade_out, 1/60.0)
        else:
            pyglet.clock.schedule_interval(self.fade_in, 1/60.0)

    def fade_out(self, dt):
        print(f"Fading out opacity :{FadeTransition.opacity}")
        FadeTransition.opacity += (255 / (self.duration * 30))
        if FadeTransition.opacity >= 255:
            pyglet.clock.unschedule(self.fade_out)
            self.is_fading = False
        self.overlay.opacity = int(FadeTransition.opacity)

    def fade_in(self, dt):
        print(f"Fading in opacity :{FadeTransition.opacity}")
        FadeTransition.opacity -= (255 / (self.duration * 60))
        if FadeTransition.opacity <= 0:
            pyglet.clock.unschedule(self.fade_in)
            self.is_fading = False
        self.overlay.opacity = int(FadeTransition.opacity)

    def draw(self):
        if self.is_fading:
            print("drawing")
            self.overlay.draw()