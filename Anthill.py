from moderngl_window import geometry
from moderngl_window.opengl.vao import VAO
import numpy as np

from Ants import Ants


class Anthill:
    def __init__(self, App, countAnt, position, size, **kwargs):
        self.App = App
        self.position = position
        self.size = size

        self.ants = Ants(App, countAnt=countAnt, startPosition=position, **kwargs)

        self.vao: VAO = None
        self.initVao()

        self.prog = self.App.load_program(
            vertex_shader='shaders/anthill/anthill_vertex_shader.glsl',
            fragment_shader='shaders/anthill/anthill_fragment_shader.glsl')

    def initVao(self):
        self.vao = geometry.quad_2d(
            size=(self.size, self.size * self.App.window_size[0] / self.App.window_size[1]),
            pos=self.position,
            attr_names=self.App.attributeNames,
            normals=False)

        uvBuffer = self.vao.get_buffer_by_name(self.App.attributeNames.TEXCOORD_0).buffer
        uvArray: np.ndarray = np.frombuffer(uvBuffer.read(), dtype=np.float32)

        uvArray = (uvArray - 0.5) * 2

        uvBuffer.write(uvArray.data)

    def render(self):
        self.vao.render(self.prog)

    def set_newResolution(self):
        width, height = self.size, self.size * self.App.window_size[0] / self.App.window_size[1]
        xPos, yPos = self.position

        # fmt: off
        pos_data = np.array([
            xPos - width / 2.0, yPos + height / 2.0, 0.0,
            xPos - width / 2.0, yPos - height / 2.0, 0.0,
            xPos + width / 2.0, yPos - height / 2.0, 0.0,
            xPos - width / 2.0, yPos + height / 2.0, 0.0,
            xPos + width / 2.0, yPos - height / 2.0, 0.0,
            xPos + width / 2.0, yPos + height / 2.0, 0.0,
        ], dtype=np.float32)

        self.vao.get_buffer_by_name(self.App.attributeNames.POSITION).buffer.write(
            pos_data.data)
