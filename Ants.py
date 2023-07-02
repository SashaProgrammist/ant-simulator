import moderngl as mgl
import moderngl_window as mglw
from moderngl_window.opengl.vao import VAO
import numpy as np
import math
from PIL import Image, ImageDraw


class Ants:
    def __init__(self, App: mglw.WindowConfig, countAnt, point_size, startPosition=(0, 0)):
        self.point_size = point_size
        self.circle = Image.new("L", (self.point_size, self.point_size), 0)
        ImageDraw.Draw(self.circle).ellipse(((0, 0),
                                             (self.point_size, self.point_size)),
                                            fill=(255,))
        self.mask = Image.new("L", (self.point_size, self.point_size), 0)
        ImageDraw.Draw(self.mask).ellipse(((0, 0),
                                           (self.point_size, self.point_size)),
                                          fill=(20,))

        self.App = App
        self.startPosition = startPosition
        self.countAnts = countAnt
        self.ants: VAO | None = None
        self.antsBuffer = self.App.ctx.buffer(reserve=self.countAnts * 2 * 4)  # buffer for vec2
        self.ants_graphic_prog = self.App.load_program(
            vertex_shader='ants_vertex_shader.glsl',
            fragment_shader='ants_fragment_shader.glsl')
        self.ants_transform_position_prog = self.App.load_program(
            vertex_shader='ants_transform_position.glsl',
            varyings=["out_position"])
        self.ants_transform_direction_prog = self.App.load_program(
            vertex_shader='ants_transform_direction.glsl',
            varyings=["out_direction"])
        self.App.set_uniform(self.ants_transform_direction_prog, "mappTexture", 1)
        self.initAnts()

    def initAnts(self):
        self.ants = VAO("ants", mode=mgl.POINTS)
        self.ants.ctx.point_size = self.point_size

        indexData = np.array(np.arange(self.countAnts),
                             dtype=np.float32)
        self.ants.buffer(indexData, "1f", ["in_index"])

        if self.startPosition == (0, 0):
            positionData = np.array(np.zeros(self.countAnts * 2),
                                    dtype=np.float32)
        else:
            positionData = np.array([np.array([self.startPosition[0]] * self.countAnts),
                                     np.array([self.startPosition[1]] * self.countAnts)],
                                    dtype=np.float32).T.reshape((self.countAnts * 2,))
        self.ants.buffer(positionData, "2f", ["in_position"])

        angelData = np.random.random((self.countAnts,)) * 2 * math.pi
        directionData = np.array([np.cos(angelData), np.sin(angelData)],
                                 dtype=np.float32).T.reshape((self.countAnts * 2,))
        self.ants.buffer(directionData, "2f", ["in_direction"])

    def set_newResolution(self):
        self.App.set_uniform(self.ants_graphic_prog, "resolution", self.App.window_size)

    def render(self):
        self.ants.render(self.ants_graphic_prog)

    def draw(self, position: np.ndarray):
        position = np.array((position + 1) / 2 * np.array(self.App.window_size) - self.point_size / 2
                            , dtype=int)

        self.App.pheromone.image.paste(self.circle,
                                       (position[0], position[1]),
                                       self.mask)

    def update(self, time, frame_time):
        self.App.set_uniform(self.ants_graphic_prog, "time", time)
        self.App.set_uniform(self.ants_graphic_prog, "frame_time", frame_time)
        self.App.set_uniform(self.ants_transform_position_prog, "time", time)
        self.App.set_uniform(self.ants_transform_position_prog, "frame_time", frame_time)
        self.App.set_uniform(self.ants_transform_direction_prog, "time", time)
        self.App.set_uniform(self.ants_transform_direction_prog, "frame_time", frame_time)

        self.ants.transform(self.ants_transform_position_prog, self.antsBuffer)
        self.ants.get_buffer_by_name("in_position").buffer.write(self.antsBuffer.read())
        self.ants.transform(self.ants_transform_direction_prog, self.antsBuffer)
        self.ants.get_buffer_by_name("in_direction").buffer.write(self.antsBuffer.read())

        buffer = self.ants.get_buffer_by_name("in_position").buffer.read()
        antsPosition = np.frombuffer(buffer, dtype=np.float32).reshape((self.countAnts, 2))

        np.apply_along_axis(lambda position: self.draw(position), 1, antsPosition)
