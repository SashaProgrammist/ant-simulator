import moderngl as mgl
from moderngl_window.opengl.vao import VAO, BufferInfo
import numpy as np
import math

from Mapp import Mapp
from Pheromone import Pheromone


class AntBufferInfo:
    def __init__(self, buffer: BufferInfo, buffer_format: str):
        self._buffer = buffer
        self.buffer_format = buffer_format

    @property
    def buffer(self):
        return self._buffer.buffer

    @property
    def attributes(self):
        return self._buffer.attributes


class Ants:
    minSpeed = 1
    maxSpeed = 1.5

    def __init__(self, App, countAnt, pointSize=30, startPosition=(0, 0)):
        self.App = App
        self.countAnts = countAnt
        self.pointSize = pointSize
        self.startPosition = startPosition
        self.ants: VAO | None = None
        self.buffers: list[AntBufferInfo] = []

        self.temporaryStorage = self.App.ctx.buffer(
            reserve=self.countAnts * 2 * 4)

        self.ants_graphic_prog = self.App.load_program(
            vertex_shader='shaders/ants/ants_vertex_shader.glsl',
            fragment_shader='shaders/ants/ants_fragment_shader.glsl')

        self.ants_transform_position_prog = self.App.load_program(
            vertex_shader='shaders/ants/ants_transform_position.glsl',
            varyings=["out_position"])
        self.ants_transform_direction_prog = self.App.load_program(
            vertex_shader='shaders/ants/ants_transform_direction.glsl',
            varyings=["out_direction"])

        self.App.mapp.set_uniformTextures(self.ants_transform_direction_prog,
                                          Mapp.mappDirection)
        for i, pheromone in enumerate(Pheromone.pheromones,
                                      Mapp.countTextures):
            self.App.set_uniform(self.ants_transform_direction_prog,
                                 pheromone.name, i)
        self.App.set_uniform(self.ants_transform_direction_prog,
                             "sensitivityThreshold", 1.5 / 255)

        self.initAnts()

    def initAnts(self):
        self.ants = VAO("ants", mode=mgl.POINTS)

        indexData = np.array(np.arange(self.countAnts),
                             dtype=np.float32)
        self.ants.buffer(indexData, "1f", ["in_index"])
        self.buffers.append(AntBufferInfo(
            self.ants.get_buffer_by_name("in_index"), "1f"))

        if self.startPosition == (0, 0):
            positionData = np.array(np.zeros(self.countAnts * 2),
                                    dtype=np.float32)
        else:
            positionData = np.array(self.startPosition * self.countAnts,
                                    dtype=np.float32).T.reshape((self.countAnts * 2,))
        self.ants.buffer(positionData, "2f", ["in_position"])
        self.buffers.append(AntBufferInfo(
            self.ants.get_buffer_by_name("in_position"), "2f"))

        angelData = np.random.random(self.countAnts) * 2 * math.pi
        directionData = np.array([np.cos(angelData), np.sin(angelData)],
                                 dtype=np.float32).T.reshape((self.countAnts * 2,))
        self.ants.buffer(directionData, "2f", ["in_direction"])
        self.buffers.append(AntBufferInfo(
            self.ants.get_buffer_by_name("in_direction"), "2f"))

        speedData = np.array(np.random.random(self.countAnts) *
                             (Ants.maxSpeed - Ants.minSpeed) + Ants.minSpeed,
                             dtype=np.float32)
        self.ants.buffer(speedData, "1f", ["in_speed"])
        self.buffers.append(AntBufferInfo(
            self.ants.get_buffer_by_name("in_speed"), "1f"))

        stackingPheromoneIndexData = \
            np.array(np.array([self.App.pheromoneHome.id] * self.countAnts),
                     dtype=np.float32)
        self.ants.buffer(stackingPheromoneIndexData, "1f", ["in_stackingPheromoneIndex"])
        self.buffers.append(AntBufferInfo(
            self.ants.get_buffer_by_name("in_stackingPheromoneIndex"), "1f"))

        pheromoneControlIndexData = \
            np.array(np.array([self.App.pheromoneFood.id] * self.countAnts),
                     dtype=np.float32)
        self.ants.buffer(pheromoneControlIndexData, "1f", ["in_pheromoneControlIndex"])
        self.buffers.append(AntBufferInfo(
            self.ants.get_buffer_by_name("in_pheromoneControlIndex"), "1f"))

    def set_newResolution(self):
        self.App.set_uniform(self.ants_graphic_prog, "resolution", self.App.window_size)

    def render(self):
        self.App.ctx.point_size = self.pointSize
        self.ants.render(self.ants_graphic_prog)

    def update(self, time, frame_time):
        self.App.set_uniform(self.ants_graphic_prog, "time", time)
        self.App.set_uniform(self.ants_graphic_prog, "frame_time", frame_time)
        self.App.set_uniform(self.ants_transform_position_prog, "time", time)
        self.App.set_uniform(self.ants_transform_position_prog, "frame_time", frame_time)
        self.App.set_uniform(self.ants_transform_direction_prog, "time", time)
        self.App.set_uniform(self.ants_transform_direction_prog, "frame_time", frame_time)

        self.ants.transform(self.ants_transform_position_prog, self.temporaryStorage)
        self.ants.get_buffer_by_name("in_position").buffer.write(self.temporaryStorage.read())
        self.ants.transform(self.ants_transform_direction_prog, self.temporaryStorage)
        self.ants.get_buffer_by_name("in_direction").buffer.write(self.temporaryStorage.read())
