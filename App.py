import logging
import moderngl as mgl
import moderngl_window as mglw
from moderngl_window import geometry
from moderngl_window.geometry.attributes import AttributeNames
from moderngl_window.timers.clock import Timer
from argparse import Namespace, ArgumentParser

from Anthill import Anthill
from Pheromone import Pheromone
from Mapp import Mapp
from DeBug import DeBug
from SaveAnimation import SaveAnimation


class App(mglw.WindowConfig):
    log_level = logging.INFO
    window_size = 1280, 720
    resource_dir = 'resources'
    fullscreen = False
    title = "ant simulator"
    cursor = True
    aspect_ratio = None
    attributeNames: AttributeNames = AttributeNames(texcoord_0="in_texCoord")
    clear_color = (1, 1, 1)
    vsync = True
    argv: Namespace = Namespace(window="pyglet")

    @classmethod
    def saveAnimation(cls, countFrame: None | int = None, name: None | str = None,
                      fps=20., fpsSim=60., invisibleFrames=2,
                      isSaveSequence=False):
        cls.vsync = False
        cls.resizable = False

        cls.__init__ = SaveAnimation.getNew__init__(
            cls, countFrame, name, fps,
            fpsSim, invisibleFrames, isSaveSequence)

        SaveAnimation.oldClose = cls.close
        cls.close = SaveAnimation.getNewClose

        cls.render = SaveAnimation.getNewRender

    @classmethod
    def add_arguments(cls, parser: ArgumentParser):
        classVars = vars(App.argv)
        for var in classVars:
            parser.add_argument('-' + var, '-' + classVars[var])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.timer: Timer = kwargs["timer"]

        self.countTextures = 0

        self.mainFbo = self.wnd.fbo
        self.fullScreen = geometry.quad_fs(self.attributeNames)

        self.deBug = DeBug(self)

        self.display_prog = self.load_program(
            vertex_shader='shaders/display/display_vertex_shader.glsl',
            fragment_shader='shaders/display/display_fragment_shader.glsl')

        self.mapp = Mapp(self)

        self.countTextures += Mapp.countTextures

        self.pheromoneWar = Pheromone(self, name="pheromoneWar", isPheromoneWar=True)
        self.pheromoneHome = Pheromone(self, name="pheromoneHome",
                                       weathering=0.99, redistribution=0.9,
                                       pointSize=4, redistributionRadius=8)
        self.pheromoneFood = Pheromone(self, name="pheromoneFood",
                                       weathering=0.99, redistribution=0.9,
                                       pointSize=4, redistributionRadius=8)

        self.pheromoneHome.addAntipode(self.pheromoneFood)
        self.pheromoneFood.addAntipode(self.pheromoneHome)

        Pheromone.initPheromoneTextureInGLSL()

        self.countTextures += Pheromone.countPheromone

        self.anthill = Anthill(App=self,
                               countAnt=500000,
                               position=(-0.84, 0.8),
                               size=0.07,
                               pointSize=4,
                               )
        self.ants = self.anthill.ants

        for pheromone in Pheromone.pheromones:
            pheromone.initAnts()

        self.set_newResolution()

        self.ctx.enable(mgl.BLEND)

    def resize(self, width: int, height: int):
        self.window_size = width, height
        self.set_newResolution()

    def key_event(self, key, action, modifiers):
        self.deBug.key_event(key, action, modifiers)

    def display(self, idTexture):
        self.set_uniform(self.display_prog, "_texture", idTexture)
        self.fullScreen.render(self.display_prog)

    def set_newResolution(self):
        self.mapp.set_newResolution()
        self.ants.set_newResolution()
        self.anthill.set_newResolution()
        for pheromone in Pheromone.pheromones:
            pheromone.set_newResolution()

    def renderVao(self):
        self.mapp.render()
        self.deBug.render()
        self.anthill.render()
        if self.deBug.isRenderAnt:
            self.ants.render()
        if self.deBug.isRenderPheromoneWar:
            for pheromone in Pheromone.pheromonesWar:
                pheromone.render()

    def update(self, time, frame_time):
        self.ants.update(time, frame_time)
        self.mapp.update(time, frame_time)
        for pheromone in Pheromone.pheromones:
            pheromone.update(time, frame_time)

    def _render(self, time, frame_time):
        if frame_time > 0.06:
            frame_time = 0.06

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
