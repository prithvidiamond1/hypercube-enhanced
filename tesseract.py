
import os
import numpy as np

import moderngl
import glfw
from glfw import GLFW

import glm

current_dir = os.path.dirname(os.path.realpath(__file__))

glfw.init()

# setting context flags
glfw.window_hint(glfw.CONTEXT_CREATION_API, glfw.NATIVE_CONTEXT_API)
glfw.window_hint(glfw.CLIENT_API, glfw.OPENGL_API)
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
glfw.window_hint(glfw.RESIZABLE, True)
glfw.window_hint(glfw.DOUBLEBUFFER, True)
glfw.window_hint(glfw.DEPTH_BITS, 24)
glfw.window_hint(glfw.SAMPLES, 8)  # For MSAA*x where x is the integer > 0

width, height = 1280, 720
window = glfw.create_window(width, height, 'GLSLtut', None, None)

glfw.make_context_current(window)
glfw.set_window_aspect_ratio(window, width, height)

ctx = moderngl.create_context(require=330)

def window_quit(window, key, scancode, action, mods):
    if key == GLFW.GLFW_KEY_ESCAPE and action == GLFW.GLFW_PRESS:
        glfw.set_window_should_close(window, GLFW.GLFW_TRUE)

def window_resize(window, w, h):
    projection = np.array(glm.perspective(45, float(w/(h+0.000001)), 1.0, 100.0), 'f4')
    prog['projection'].write(projection)
    ctx.viewport = (0, 0, w, h)

glfw.set_key_callback(window, window_quit)
glfw.set_window_size_callback(window, window_resize)

glfw.swap_interval(1) # Toggles V-sync, 0 = Off, 1 = On, Which means it also unlocks/locks the framerate

prog = ctx.program(
    vertex_shader=open(f'{current_dir}\\prog.vert', 'r').read(),
    fragment_shader=open(f'{current_dir}\\prog.frag', 'r').read()
    )

vertices = np.zeros(66, [('positions', 'f4', 4)])
vertices['positions'] = [(-1, 1, 1, 1), (-1, 1, -1, 1),
                         (-1, 1, -1, 1), (-1, 1, -1, -1),
                         (1, 1, -1, 1), (1, 1, -1, -1),
                         (1, -1, 1, 1), (-1, -1, 1, 1),
                         (-1, -1, 1, 1), (-1, -1, -1, 1),
                         (-1, -1, -1, 1), (1, -1, -1, 1),
                         (1, -1, -1, 1), (1, -1, 1, 1),
                         (1, -1, 1, 1), (1, 1, 1, 1),
                         (1, 1, 1, 1), (1, 1, 1, -1),
                         (-1, 1, -1, 1), (1, 1, -1, 1),
                         (-1, 1, -1, 1), (-1, 1, 1, 1),
                         (1, 1, -1, 1), (1, -1, -1, 1),
                         (1, 1, -1, 1), (1, 1, 1, 1),
                         (-1, 1, -1, 1), (-1, -1, -1, 1),
                         (-1, -1, 1, 1), (-1, -1, 1, -1),
                         (-1, -1, -1, -1), (-1, -1, -1, 1),
                         (1, -1, -1, -1), (1, -1, -1, 1),
                         (1, -1, 1, -1), (1, -1, 1, 1),
                         (-1, 1, 1, -1), (-1, 1, 1, 1),
                         (1, 1, 1, 1), (-1, 1, 1, 1),
                         (-1, -1, 1, 1), (-1, 1, 1, 1),
                         (-1, 1, -1, -1), (-1, 1, 1, -1),
                         (-1, 1, -1, -1), (1, 1, -1, -1),
                         (1, -1, -1, -1), (1, 1, -1, -1),
                         (1, -1, 1, -1), (1, -1, -1, -1),
                         (-1, -1, 1, -1), (1, -1, 1, -1),
                         (1, 1, 1, -1), (1, 1, -1, -1),
                         (-1, -1, -1, -1), (-1, -1, 1, -1),
                         (1, 1, 1, -1), (-1, 1, 1, -1),
                         (-1, -1, -1, -1), (1, -1, -1, -1),
                         (1, 1, 1, -1), (1, -1, 1, -1),
                         (-1, -1, -1, -1), (-1, 1, -1, -1),
                         (-1, 1, 1, -1), (-1, -1, 1, -1)]

projection = np.array(glm.perspective(45, width/(height+0.000001), 1.0, 100.0), 'f4')
view = np.eye(4, dtype='f4')
model = np.eye(4, dtype='f4')

model = glm.translate(model, np.array([0, 0, -4], 'f4'))
model = glm.rotate(model, 4.36, np.array([0, 1, 0], 'f4'))

prog['projection'].write(projection)
prog['view'].write(view)
prog['model'].write(model)

vbo = ctx.buffer(vertices)
vao = ctx.vertex_array(prog, ((vbo, '4f', 'position'),))

ctx.enable(ctx.DEPTH_TEST)

# ctx.wireframe = True

theta = 0

while not glfw.window_should_close(window):
    ctx.screen.use()
    ctx.screen.clear(1.0, 1.0, 1.0, 1.0)

    theta += 0.02

    db_rotation = np.array(([np.cos(theta), (np.sin(theta)), 0, 0],
                    [-(np.sin(theta)), np.cos(theta), 0, 0],
                    [0, 0, np.cos(theta), -(np.sin(theta))],
                    [0, 0, np.sin(theta), np.cos(theta)]), 'f4')
    
    prog['dbr'].write(db_rotation)

    vao.render(moderngl.LINES)

    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.destroy_window(window)
