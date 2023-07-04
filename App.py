import logging
import moderngl as mgl
import moderngl_window as mglw
from moderngl_window import geometry
from moderngl_window.geometry.attributes import AttributeNames
from moderngl_window.opengl.vao import VAO
import cv2
import os
import shutil
import numpy as np

from Ants import Ants
from Pheromone import Pheromone
from Mapp import Mapp


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


def sequenceToVideo(image_folder, video_name):
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), 60, (width, height))
    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))
    cv2.destroyAllWindows()
    video.release()


class App(mglw.WindowConfig):
    log_level = logging.INFO
    window_size = 1600, 900
    resource_dir = 'resources'
    fullscreen = False
    title = "ant simulator"
    cursor = True
    aspect_ratio = None
    attributeNames = AttributeNames(texcoord_0="in_texCoord")
    indexFrame: int = None
    countFrame: int = None
    ctx: mgl.Context = None
    textureFbo: mgl.Texture = None
    fbo: mgl.Framebuffer = None
    textureConvert: mgl.Texture = None
    Convert: mgl.Framebuffer = None
    prog: mgl.Program = None
    quad: VAO = None

    @classmethod
    def initBuffersForSaveImage(cls, self):
        cls.ctx = self.ctx
        cls.textureFbo = cls.ctx.texture(cls.window_size, 4)
        cls.textureFbo.use(location=Mapp.countTextures + Pheromone.countPheromone)
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
        cls.quad = geometry.quad_fs(cls.attributeNames)

    @classmethod
    def saveAnimation(cls, countFrame=None, name=None):
        cls.indexFrame = 0
        cls.countFrame = countFrame
        delFolder("animation/animationTemp")

        def render(self: cls, *_):
            if cls.ctx is None:
                cls.initBuffersForSaveImage(self)

            cls._render(self, cls.indexFrame / 60, 1 / 60)

            cls.textureFbo.write(self.ctx.fbo.read(components=4, dtype='f1'))
            cls.Convert.use()
            cls.quad.render(cls.prog)
            self.ctx.fbo.use()

            path = f"animation/animationTemp/{'0' * (len(str(cls.countFrame)) - len(str(cls.indexFrame)))}" \
                   f"{cls.indexFrame}.png"
            raw = cls.Convert.read(components=4, dtype='f1')
            buf: np.ndarray = np.frombuffer(raw, dtype='uint8'). \
                reshape((*self.ctx.fbo.size[1::-1], 4))
            cv2.imwrite(path, buf)

            cls.indexFrame += 1

            if cls.countFrame is not None and cls.indexFrame >= cls.countFrame:
                self.wnd.is_closing = True

                sequenceToVideo("animation/animationTemp",
                                f'animation/saveAnimation/'
                                f'{cls.countFrame if name is None else name}.avi')

        cls.render = render

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.deBag_quad = geometry.quad_fs(self.attributeNames)
        self.deBag_prog = self.load_program(
            vertex_shader='shaders/deBag/deBag_vertex_shader.glsl',
            fragment_shader='shaders/deBag/deBag_fragment_shader.glsl')
        self.set_uniform(self.deBag_prog, "_texture", 3)

        self.mapp = Mapp(self)

        self.pheromoneWar = Pheromone(self, name="pheromoneWar", isPheromoneWar=True)
        self.pheromoneHome = Pheromone(self, name="pheromoneHome")
        self.pheromoneFood = Pheromone(self, name="pheromoneFood")

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
        self.mapp.set_newResolution()
        self.set_uniform(self.deBag_prog, "resolution", self.window_size)
        self.ants.set_newResolution()
        for pheromone in Pheromone.pheromones:
            pheromone.set_newResolution()

    def renderVao(self):
        self.mapp.render()
        self.deBag_quad.render(self.deBag_prog)
        self.ants.render()
        for pheromone in Pheromone.pheromones:
            pheromone.render()

    def update(self, time, frame_time):
        self.ants.update(time, frame_time)
        for pheromone in Pheromone.pheromones:
            pheromone.update(time, frame_time)

    def _render(self, time, frame_time):
        if frame_time > 0.04:
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
