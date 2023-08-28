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


class TemporaryStorages:
    def __init__(self, App, ants):
        self.App = App
        self.ants = ants
        self.storages = dict()

    def get(self, countFourBate):
        if countFourBate not in self.storages:
            self.storages[countFourBate] = self.App.ctx.buffer(
                reserve=self.ants.countAnts * countFourBate * 4)

        return self.storages[countFourBate]


class Ants:
    minSpeed = 0.2
    maxSpeed = 0.3

    def __init__(self, App, countAnt, pointSize=30, startPosition=(0, 0)):
        self.App = App
        self.countAnts = countAnt
        self.pointSize = pointSize
        self.startPosition = startPosition
        self.ants: VAO | None = None
        self.buffers: list[AntBufferInfo] = []

        self.temporaryStorages = TemporaryStorages(App, self)

        self.ants_graphic_prog = self.App.load_program(
            vertex_shader='shaders/ants/ants_vertex_shader.glsl',
            fragment_shader='shaders/ants/ants_fragment_shader.glsl')

        self.ants_transform_position_prog = self.App.load_program(
            vertex_shader='shaders/ants/ants_transform_position.glsl',
            varyings=["out_position"])
        self.ants_transform_direction_prog = self.App.load_program(
            vertex_shader='shaders/ants/ants_transform_direction.glsl',
            varyings=["out_direction"])
        self.changePheromone_varyings = ["out_pheromoneControlIndex",
                                         "out_stackingPheromoneIndex",
                                         "out_isDirectionChanged",
                                         "out_time"]
        self.ants_transform_changePheromone_prog = self.App.load_program(
            vertex_shader='shaders/ants/ants_transform_changePheromone.glsl',
            varyings=self.changePheromone_varyings)

        self.App.set_uniform(self.ants_graphic_prog, "foodPheromone",
                             self.App.pheromoneFood.id)

        self.App.mapp.set_uniformTextures(self.ants_transform_direction_prog,
                                          Mapp.mappDirection)
        for pheromone in Pheromone.pheromones:
            self.App.set_uniform(self.ants_transform_direction_prog,
                                 pheromone.name, pheromone.idTexture)
        self.App.set_uniform(self.ants_transform_direction_prog,
                             "sensitivityThreshold", 1.5 / 255)

        self.App.set_uniform(self.ants_transform_changePheromone_prog,
                             "foodPheromone", self.App.pheromoneFood.id)
        self.App.set_uniform(self.ants_transform_changePheromone_prog,
                             "homePheromone", self.App.pheromoneHome.id)
        self.App.set_uniform(self.ants_transform_changePheromone_prog,
                             "homePosition", self.startPosition)
        self.App.mapp.set_uniformTextures(self.ants_transform_changePheromone_prog,
                                          Mapp.mappTexture)

        self.initAnts()

        self.transformInUpdate = ["position",
                                  "direction"]
        self.dimensionTransform = {"position": 2,
                                   "direction": 2}

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
        self.ants.buffer(positionData,
                         "2f",
                         ["in_position"])
        self.buffers.append(AntBufferInfo(
            self.ants.get_buffer_by_name("in_position"), "2f"))

        angelData = np.random.random(self.countAnts) * 2 * math.pi
        directionData = np.array([np.cos(angelData), np.sin(angelData)],
                                 dtype=np.float32).T.reshape((self.countAnts * 2,))
        self.ants.buffer(directionData,
                         "2f",
                         ["in_direction"])
        self.buffers.append(AntBufferInfo(
            self.ants.get_buffer_by_name("in_direction"), "2f"))

        speedData = np.array(np.random.random(self.countAnts) *
                             (Ants.maxSpeed - Ants.minSpeed) + Ants.minSpeed,
                             dtype=np.float32)
        self.ants.buffer(speedData,
                         "1f",
                         ["in_speed"])
        self.buffers.append(AntBufferInfo(
            self.ants.get_buffer_by_name("in_speed"), "1f"))

        stackingPheromoneIndexData = \
            np.array([self.App.pheromoneHome.id] * self.countAnts, dtype=np.float32)
        self.ants.buffer(stackingPheromoneIndexData,
                         "1f",
                         ["in_stackingPheromoneIndex"])
        self.buffers.append(AntBufferInfo(
            self.ants.get_buffer_by_name("in_stackingPheromoneIndex"), "1f"))

        pheromoneControlIndexData = \
            np.array([self.App.pheromoneFood.id] * self.countAnts, dtype=np.float32)
        self.ants.buffer(pheromoneControlIndexData,
                         "1f",
                         ["in_pheromoneControlIndex"])
        self.buffers.append(AntBufferInfo(
            self.ants.get_buffer_by_name("in_pheromoneControlIndex"), "1f"))

        isDirectionChangedData = np.array(np.zeros(self.countAnts),
                                          dtype=np.float32)
        self.ants.buffer(isDirectionChangedData,
                         "1f",
                         ["in_isDirectionChanged"])
        self.buffers.append(AntBufferInfo(
            self.ants.get_buffer_by_name("in_isDirectionChanged"), "1f"))

        timeData = np.array(np.zeros(self.countAnts), dtype=np.float32)
        self.ants.buffer(timeData, "1f", ["in_time"])
        self.buffers.append(AntBufferInfo(
            self.ants.get_buffer_by_name("in_time"), "1f"))

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
        self.App.set_uniform(self.ants_transform_changePheromone_prog, "frame_time", frame_time)

        count = len(self.changePheromone_varyings)
        self.ants.transform(self.ants_transform_changePheromone_prog,
                            self.temporaryStorages.get(count))
        controlStackingIndex: np.ndarray = \
            np.frombuffer(self.temporaryStorages.get(count).read(), dtype=np.float32)
        for i, name in enumerate(self.changePheromone_varyings):
            (self.ants.get_buffer_by_name(name.replace("out", "in"))
             .buffer.write(np.array(controlStackingIndex[i::count]).data))

        for name in self.transformInUpdate:
            self.ants.transform(getattr(self, f"ants_transform_{name}_prog"),
                                self.temporaryStorages.get(
                                    self.dimensionTransform[name]))
            (self.ants.get_buffer_by_name(f"in_{name}").
             buffer.write(self.temporaryStorages.get(
                self.dimensionTransform[name]).read()))
