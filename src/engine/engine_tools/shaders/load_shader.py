from pyglet import gl



def import_shader():
    # Load and compile the vertex shader and fragment shader
    vertex_shader_source = open('vertex_shader.glsl').read()
    fragment_shader_source = open('bloom_shader.glsl').read()
    shader = gl.Shader(vertex_shader_source, fragment_shader_source)


    # Get the uniform locations for the shader parameters
    threshold_loc = gl.glGetUniformLocation(shader.handle, b'threshold')
    exposure_loc = gl.glGetUniformLocation(shader.handle, b'exposure')
    decay_loc = gl.glGetUniformLocation(shader.handle, b'decay')
    numRays_loc = gl.glGetUniformLocation(shader.handle, b'numRays')
