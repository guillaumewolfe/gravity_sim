import pyglet

class GameStateManager:
    def __init__(self):
        self.state_stack = []

    def push_state(self,state):
        self.state_stack.append(state)
    
    def pop_state(self):
        return self.state_stack.pop()
    
    def update(self,dt):
        if self.state_stack:
            self.state_stack[-1].update(dt)

    def draw(self):
        for state in self.state_stack:
            state.draw()