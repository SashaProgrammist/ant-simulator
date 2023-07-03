import logging
import moderngl as mgl
import moderngl_window as mglw
from moderngl_window import geometry
from moderngl_window.geometry.attributes import AttributeNames
from PIL import Image
import os
import shutil

from Ants import Ants
from Pheromone import Pheromone
from Mapp import Mapp


class App(mglw.WindowConfig):
    log_level = logging.INFO
    window_size = 1600, 900
    resource_dir = 'shaders'
    fullscreen = False
    title = "ant simulator"
    cursor = True
    aspect_ratio = None
    attributeNames = AttributeNames(texcoord_0="in_texCoord")
    indexFrame = None

    @classmethod
    def saveAnimation(cls):
        cls.indexFrame = 0

        def render(self: cls, time, frame_time):
            cls._render(self, time, frame_time)

            if cls.indexFrame % 2:
                Image.frombytes('RGB', self.ctx.fbo.size,
                                self.ctx.fbo.read(), 'raw',
                                'RGB', 0, -1).save(f"animation/{cls.indexFrame // 2}.png")
            cls.indexFrame += 1

        cls.render = render

        folder = "animation"
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.global_quad = geometry.quad_fs(self.attributeNames)
        self.global_prog = self.load_program(
            vertex_shader='global_vertex_shader.glsl',
            fragment_shader='global_fragment_shader.glsl')
        self.set_uniform(self.global_prog, "_texture", 2)

        self.mapp = Mapp(self)

        self.pheromone = Pheromone(self, isPheromoneWar=False,
                                   weathering=0.99, redistribution=0.1,
                                   redistributionRadius=5)

        Pheromone.initPheromoneTextureInGLSL()

        self.ants = Ants(self, 100000, pointSize=5, startPosition=(-0., 0.))

        for pheromone in Pheromone.pheromones:
            pheromone.initAnts()

        self.set_newResolution()

        self.ctx.enable(mgl.BLEND)

    def resize(self, width: int, height: int):
        self.window_size = width, height
        self.set_newResolution()

    def set_newResolution(self):
        self.mapp.set_newResolution()
        self.set_uniform(self.global_prog, "resolution", self.window_size)
        self.ants.set_newResolution()
        self.pheromone.set_newResolution()

    def renderVao(self):
        self.mapp.render()
        self.global_quad.render(self.global_prog)
        # self.ants.render()
        self.pheromone.render()

    def update(self, time, frame_time):
        self.ants.update(time, frame_time)
        self.pheromone.update(time, frame_time)

    def _render(self, time, frame_time):
        if frame_time > 0.03:
            frame_time = 0

        self.ctx.clear()

        self.update(time, frame_time)

        self.renderVao()

    def render(self, time, frame_time):
        self._render(time, frame_time)

    @staticmethod
    def set_uniform(prog, name, value):
        try:
            prog[name] = value
        except KeyError:
            # print(f"uniform: {name} - not in ")
            pass
