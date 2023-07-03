import logging

import moderngl as mgl
import moderngl_window as mglw
from moderngl_window import geometry
from moderngl_window.geometry.attributes import AttributeNames
from Ants import Ants
from Pheromone import Pheromone


class App(mglw.WindowConfig):
    log_level = logging.INFO
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
        self.set_uniform(self.global_prog, "pheromone", 1)

        self.mapp_quad = geometry.quad_fs(self.attributeNames)
        self.mapp_texture = self.load_texture_2d("../mapp/mapp.png")
        self.mappTextureID = 0
        self.mapp_texture.use(location=self.mappTextureID)
        self.mapp_prog = self.load_program(
            vertex_shader='mapp_vertex_shader.glsl',
            fragment_shader='mapp_fragment_shader.glsl')
        self.set_uniform(self.mapp_prog, "mappTexture", self.mappTextureID)

        self.pheromone = Pheromone(self, isPheromoneWar=False,
                                   weathering=0.99, redistribution=0.9,
                                   redistributionRadius=5)

        Pheromone.initPheromoneTextureInGLSL()

        self.ants = Ants(self, 100000, pointSize=5, startPosition=(-0.8, 0.8))

        for pheromone in Pheromone.pheromones:
            pheromone.initAnts()

        self.set_newResolution()

        self.ctx.enable(mgl.BLEND)

    def resize(self, width: int, height: int):
        self.window_size = width, height
        self.set_newResolution()

    def set_newResolution(self):
        self.set_uniform(self.mapp_prog, "resolution", self.window_size)
        self.set_uniform(self.global_prog, "resolution", self.window_size)
        self.ants.set_newResolution()
        self.pheromone.set_newResolution()

    def _render(self):
        self.mapp_quad.render(self.mapp_prog)
        self.global_quad.render(self.global_prog)
        self.ants.render()
        self.pheromone.render()

    def update(self, time, frame_time):
        self.ants.update(time, frame_time)
        self.pheromone.update(time, frame_time)

    def render(self, time, frame_time):
        if frame_time > 0.03:
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
