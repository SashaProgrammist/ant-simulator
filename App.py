import moderngl as mgl
import moderngl_window as mglw
from moderngl_window import geometry
from moderngl_window.opengl.vao import VAO
from moderngl_window.geometry.attributes import AttributeNames
import numpy as np
import math


class App(mglw.WindowConfig):
    window_size = 1600, 900
    resource_dir = 'shaders'
    fullscreen = False
    title = "ant simulator"
    cursor = True
    aspect_ratio = None
    attributeNames = AttributeNames(texcoord_0="in_texCoord")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.global_quad = geometry.quad_fs(self.attributeNames)
        self.global_prog = self.load_program(
            vertex_shader='global_vertex_shader.glsl',
            fragment_shader='global_fragment_shader.glsl')
        self.set_uniform(self.global_prog, "mappTexture", 1)

        self.mapp_quad = geometry.quad_fs(self.attributeNames)
        self.mapp_texture = self.load_texture_2d("../mapp/mapp.png")
        self.mapp_texture.use(location=1)
        self.mapp_prog = self.load_program(
            vertex_shader='mapp_vertex_shader.glsl',
            fragment_shader='mapp_fragment_shader.glsl')
        self.set_uniform(self.mapp_prog, "mappTexture", 1)

        self.countAnts = 100000
        self.ants: VAO | None = None
        self.antsBuffer = self.ctx.buffer(reserve=self.countAnts * 2 * 4)  # buffer for vec2
        self.ants_graphic_prog = self.load_program(
            vertex_shader='ants_vertex_shader.glsl',
            fragment_shader='ants_fragment_shader.glsl')
        self.ants_transform_position_prog = self.load_program(
            vertex_shader='ants_transform_position.glsl',
            varyings=["out_position"])
        self.ants_transform_direction_prog = self.load_program(
            vertex_shader='ants_transform_direction.glsl',
            varyings=["out_direction"])
        self.set_uniform(self.ants_transform_direction_prog, "mappTexture", 1)
        self.initAnts()

        self.set_newResolution()

        self.ctx.enable(mgl.BLEND)

    def initAnts(self):
        self.ants = VAO("ants", mode=mgl.POINTS)
        self.ants.ctx.point_size = 5

        indexData = np.array(np.arange(self.countAnts),
                             dtype=np.float32)
        self.ants.buffer(indexData, "1f", ["in_index"])

        positionData = np.array(np.zeros(self.countAnts * 2),
                                dtype=np.float32)
        self.ants.buffer(positionData, "2f", ["in_position"])

        angelData = np.random.random((self.countAnts,)) * 2 * math.pi
        directionData = np.array([np.cos(angelData), np.sin(angelData)],
                                 dtype=np.float32).T.reshape((self.countAnts * 2,))
        self.ants.buffer(directionData, "2f", ["in_direction"])

    def resize(self, width: int, height: int):
        self.window_size = width, height
        self.set_newResolution()

    def set_newResolution(self):
        self.set_uniform(self.mapp_prog, "resolution", self.window_size)
        self.set_uniform(self.global_prog, "resolution", self.window_size)
        self.set_uniform(self.ants_graphic_prog, "resolution", self.window_size)

    def _render(self):
        self.mapp_quad.render(self.mapp_prog)
        self.global_quad.render(self.global_prog)
        self.ants.render(self.ants_graphic_prog)

    def update(self, time, frame_time):
        self.set_uniform(self.ants_graphic_prog, "time", time)
        self.set_uniform(self.ants_graphic_prog, "frame_time", frame_time)
        self.set_uniform(self.ants_transform_position_prog, "time", time)
        self.set_uniform(self.ants_transform_position_prog, "frame_time", frame_time)
        self.set_uniform(self.ants_transform_direction_prog, "time", time)
        self.set_uniform(self.ants_transform_direction_prog, "frame_time", frame_time)

        self.ants.transform(self.ants_transform_position_prog, self.antsBuffer)
        self.ants.get_buffer_by_name("in_position").buffer.write(self.antsBuffer.read())
        self.ants.transform(self.ants_transform_direction_prog, self.antsBuffer)
        self.ants.get_buffer_by_name("in_direction").buffer.write(self.antsBuffer.read())

    def render(self, time, frame_time):
        if frame_time > 0.0625:
            frame_time = 0

        self.ctx.clear()

        self.update(time, frame_time)

        self._render()

    @staticmethod
    def set_uniform(prog, name, value):
        try:
            prog[name] = value
        except KeyError:
            # print(f"uniform: {name} - not in ")
            pass
