from ctypes import byref
from pyglet.gl import *
from pyglet.text import Label

class FrameBuffer:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Generate frame buffer
        self.fbo = GLuint()
        glGenFramebuffers(1, self.fbo)
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)

        # Generate texture
        self.texture = GLuint()
        glGenTextures(1, self.texture)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glBindTexture(GL_TEXTURE_2D, 0)

        # Attach it to FBO
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.texture, 0)

        # Create the depth buffer
        self.depth_buffer = GLuint()
        glGenRenderbuffers(1, byref(self.depth_buffer))
        glBindRenderbuffer(GL_RENDERBUFFER, self.depth_buffer)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT24, width, height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self.depth_buffer)
        
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            print("Failed to create framebuffer!")


        # Unbind
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def bind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)

    def unbind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
    
    def draw(self, x, y):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(x, y)
        glTexCoord2f(1, 0); glVertex2f(x + self.width, y)
        glTexCoord2f(1, 1); glVertex2f(x + self.width, y + self.height)
        glTexCoord2f(0, 1); glVertex2f(x, y + self.height)
        glEnd()
        glDisable(GL_TEXTURE_2D)

