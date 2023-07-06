import logging
import moderngl as mgl
import moderngl_window as mglw
from moderngl_window import geometry
from moderngl_window.geometry.attributes import AttributeNames
from moderngl_window.opengl.vao import VAO
from moderngl_window.context.base.window import logger
from moderngl_window.timers.clock import Timer
import cv2
import os
import shutil
import numpy as np

from Ants import Ants
from Pheromone import Pheromone
from Mapp import Mapp
from DeBug import DeBug


def delFolder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


class App(mglw.WindowConfig):
    log_level = logging.INFO
    window_size = 1280, 720
    resource_dir = 'resources'
    fullscreen = False
    title = "ant simulator"
    cursor = True
    aspect_ratio = None
    attributeNames = AttributeNames(texcoord_0="in_texCoord")
    clear_color = (1, 1, 1)
    vsync = True

    indexFrame: int
    indexSimFrame: int
    countFrame: int
    fps: float
    framesSim: int
    isSaveSequence: bool
    fpsSim: float
    video: cv2.VideoWriter
    ctx: mgl.Context
    textureFbo: mgl.Texture
    textureFboId: int
    fbo: mgl.Framebuffer
    textureConvert: mgl.Texture
    Convert: mgl.Framebuffer
    prog: mgl.Program
    quad: VAO
    buffers: list[np.ndarray]

    @classmethod
    def initSaveAnimation(cls, self, countFrame, name,
                          fps, fpsSim, invisibleFrames, isSaveSequence):
        cls.indexFrame = 0
        cls.indexSimFrame = 0
        cls.countFrame = countFrame
        cls.fps = fps
        cls.framesSim = invisibleFrames + 1
        cls.isSaveSequence = isSaveSequence
        cls.fpsSim = fpsSim
        cls.video = cv2.VideoWriter(
            f'animation/saveAnimation/{name}.avi',
            cv2.VideoWriter_fourcc(*'mp4v'), cls.fps,
            cls.window_size)
        cls.ctx = self.ctx
        cls.textureFbo = cls.ctx.texture(cls.window_size, 4, dtype="f1")
        cls.textureFboId = Mapp.countTextures + Pheromone.countPheromone
        cls.textureFbo.use(location=cls.textureFboId)
        cls.textureConvert = cls.ctx.texture(cls.window_size, 4)
        cls.Convert = cls.ctx.framebuffer(cls.textureConvert)
        cls.prog = cls.ctx.program(
            vertex_shader="#version 400\n"
                          "in vec3 in_position;\n"
                          "in vec2 in_texCoord;\n"
                          "out vec2 v_texCoord;\n"
                          "void main() {\n"
                          "    gl_Position = vec4(in_position, 1);\n"
                          "    v_texCoord = in_texCoord;\n"
                          "}\n",
            fragment_shader="#version 400\n"
                            "in vec2 v_texCoord;\n"
                            "uniform sampler2D _textureFbo;\n"
                            "out vec4 fragColor;\n"
                            "void main() {\n"
                            "    fragColor = "
                            "vec4(texture(_textureFbo, v_texCoord * vec2(1, -1)).bgr, 1);\n"
                            "}\n")
        cls.prog["_textureFbo"] = Mapp.countTextures + Pheromone.countPheromone
        cls.quad = self.fullScreen
        cls.buffers = []

    @classmethod
    def saveAnimation(cls, countFrame: None | int = None, name: None | str = None,
                      fps=20., fpsSim=60., invisibleFrames=2,
                      isSaveSequence=False):
        cls.vsync = False

        if isSaveSequence:
            delFolder("animation/animationTemp")

        close = cls.close

        def newClose(self):
            close(self)
            App.video.release()

            unitTimes = [60, 60, 24, 30, 12]
            unitTimesNames = ["m", "h", "d", "m", "e"]
            i = 0
            time = self.timer.time
            timeSim = cls.indexSimFrame / cls.fpsSim
            unitTime = "s"
            while i < len(unitTimes) and timeSim >= unitTimes[i]:
                timeSim /= unitTimes[i]
                unitTime = unitTimesNames[i]
                i += 1

            logger.info(f"time in sim: {timeSim:.2f} {unitTime} @ "
                        f"{cls.indexFrame / time * cls.framesSim:.2f} ups")

        cls.close = newClose

        def render(self: cls, *_):
            if not hasattr(cls, "indexFrame"):
                cls.initSaveAnimation(
                    self, countFrame,
                    (str(countFrame) if countFrame is not None else "video")
                    if name is None else name,
                    fps, fpsSim, invisibleFrames, isSaveSequence)

            time, frameTime = cls.indexSimFrame / cls.fpsSim, 1 / cls.fpsSim
            self.ctx.clear()
            for i in range(cls.framesSim):
                self.update(time, frameTime)
                cls.indexSimFrame += 1
                time = cls.indexSimFrame / cls.fpsSim

            self.renderVao()

            cls.textureFbo.write(self.ctx.fbo.read(components=4))
            cls.Convert.use()
            cls.quad.render(cls.prog)
            self.mainFbo.use()

            raw = cls.Convert.read(components=3, dtype='f1')
            buf: np.ndarray = np.frombuffer(raw, dtype='uint8'). \
                reshape((*self.ctx.fbo.size[1::-1], 3))
            cls.buffers.append(buf)

            if cls.isSaveSequence:
                path = f"animation/animationTemp/" + \
                       '0' * (len(str(cls.countFrame // cls.framesSim)) -
                              len(str(cls.indexFrame))) + \
                       f"{cls.indexFrame}.png"
                cv2.imwrite(path, buf)

            cls.video.write(buf)

            if cls.countFrame is not None and cls.indexFrame >= cls.countFrame:
                self.wnd.is_closing = True

                cls.video.release()

                cls.close(self)

            cls.indexFrame += 1

        cls.render = render

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.timer: Timer = kwargs["timer"]

        self.mainFbo = self.wnd.fbo
        self.fullScreen = geometry.quad_fs(self.attributeNames)

        self.deBug = DeBug(self)

        self.display_prog = self.load_program(
            vertex_shader='shaders/display/display_vertex_shader.glsl',
            fragment_shader='shaders/display/display_fragment_shader.glsl')

        self.mapp = Mapp(self)

        self.pheromoneWar = Pheromone(self, name="pheromoneWar", isPheromoneWar=True)
        self.pheromoneHome = Pheromone(self, name="pheromoneHome",
                                       weathering=0.9, redistribution=0.4,
                                       pointSize=4)
        self.pheromoneFood = Pheromone(self, name="pheromoneFood")

        self.pheromoneHome.addAntipode(self.pheromoneFood)
        self.pheromoneFood.addAntipode(self.pheromoneHome)

        Pheromone.initPheromoneTextureInGLSL()

        self.ants = Ants(self, 500000, pointSize=4, startPosition=(-0.8, 0.8))

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
        for pheromone in Pheromone.pheromones:
            pheromone.set_newResolution()

    def renderVao(self):
        self.mapp.render()
        self.deBug.render()
        if self.deBug.isRenderAnt:
            self.ants.render()
        for pheromone in Pheromone.pheromonesWar:
            pheromone.render()

    def update(self, time, frame_time):
        self.ants.update(time, frame_time)
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
