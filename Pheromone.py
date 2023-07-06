import moderngl as mgl
import moderngl_window as mglw
from moderngl_window import geometry
from moderngl_window.opengl.vao import VAO

from Mapp import Mapp


class Pheromone:
    countPheromone = 0
    pheromones = []

    def __init__(self, App, windowSkele=0.5, pointSize=None,
                 name=None, isPheromoneWar=False,
                 weathering=0.99, redistribution=0.1, redistributionRadius=2):
        self.App = App
        self.windowSkele = windowSkele
        if pointSize is not None:
            self.pointSize = pointSize
        else:
            if isPheromoneWar:
                self.pointSize = 25
            else:
                self.pointSize = 3
        if name is not None:
            self.name = name
        else:
            self.name = f"pheromone_{Pheromone.countPheromone}"
        self.isPheromoneWar = isPheromoneWar
        self.weathering = weathering
        self.redistribution = redistribution
        self.redistributionRadius = redistributionRadius

        self.id = Pheromone.countPheromone

        self.windowSize = tuple(int(size * self.windowSkele)
                                for size in self.App.window_size)
        self.texture: mgl.Texture = self.App.ctx.texture(
            self.windowSize,
            2, dtype="f1")
        self.idTexture = Pheromone.countPheromone + self.App.mapp.countTextures
        self.texture.use(self.idTexture)

        self.fbo: mgl.Framebuffer = self.App.ctx.framebuffer(self.texture)
        if not self.isPheromoneWar:
            self.fbo.use()
            self.App.ctx.clear(0.5, 0.5)
            self.App.mainFbo.use()

        self.ants: VAO = VAO(self.name, mode=mgl.POINTS)

        self.fullScreen = self.App.fullScreen

        self.displayAnts_prog = self.App.load_program(
            vertex_shader="shaders/pheromone/pheromone_display_ants_vertex_shader.glsl",
            fragment_shader="shaders/pheromone/pheromone_display_ants_fragment_shader.glsl")
        self.App.set_uniform(self.displayAnts_prog, "isPheromoneWar", self.isPheromoneWar)
        self.App.set_uniform(self.displayAnts_prog, "pheromone", Pheromone.countPheromone)
        self.App.set_uniform(self.displayAnts_prog, "pheromoneSampler", self.idTexture)

        if not self.isPheromoneWar:
            self.pheromoneUpdate_prog = self.App.load_program(
                vertex_shader="shaders/pheromone/pheromone_update_vertex_shader.glsl",
                fragment_shader="shaders/pheromone/pheromone_update_fragment_shader.glsl")
            self.App.mapp.set_uniformTextures(self.pheromoneUpdate_prog, Mapp.mappTexture)
            self.App.set_uniform(self.pheromoneUpdate_prog, "pheromoneTexture", self.idTexture)
            self.updateWeatheringRedistribution(1, 1)
            self.App.set_uniform(self.pheromoneUpdate_prog, "redistributionRadius",
                                 self.redistributionRadius)

            self.pheromoneWar_prog = None
        else:
            self.pheromoneWar_prog = self.App.load_program(
                vertex_shader="shaders/pheromone/pheromone_war_vertex_shader.glsl",
                fragment_shader="shaders/pheromone/pheromone_war_fragment_shader.glsl")
            self.App.set_uniform(self.pheromoneWar_prog, "pheromone", self.idTexture)

            self.pheromoneUpdate_prog = None

        Pheromone.countPheromone += 1
        Pheromone.pheromones.append(self)

    def initAnts(self):
        buffers = self.App.ants.buffers
        for buffer in buffers:
            self.ants.buffer(buffer.buffer, buffer.buffer_format, buffer.attributes)

    def set_newResolution(self):
        newWindowSize = tuple(int(size * self.windowSkele) for size in self.App.window_size)

        if newWindowSize != self.windowSize:
            newTexture = self.App.ctx.texture(
                tuple(int(size * self.windowSkele) for size in self.App.window_size),
                2, dtype="f1")
            newFbo = self.App.ctx.framebuffer(newTexture)
            newFbo.use()

            self.App.display(self.idTexture)

            self.fbo.release()
            self.texture.release()

            self.windowSize = newWindowSize
            self.fbo = newFbo
            self.texture = newTexture
            newTexture.use(self.idTexture)

            self.App.mainFbo.use()

        self.App.set_uniform(self.displayAnts_prog, "resolution",
                             newWindowSize)
        if not self.isPheromoneWar:
            self.App.set_uniform(self.pheromoneUpdate_prog, "resolution",
                                 self.App.window_size)

    def updateWeatheringRedistribution(self, frame_time, timeScale=0.1):
        frame_time /= timeScale
        weathering = self.weathering ** frame_time
        redistribution = 1 - (1 - self.redistribution) ** frame_time

        weathering -= redistribution
        redistribution /= (self.redistributionRadius * 2 + 1) ** 2 - 1

        self.App.set_uniform(self.pheromoneUpdate_prog, "weathering",
                             weathering)
        self.App.set_uniform(self.pheromoneUpdate_prog, "redistribution",
                             redistribution)

    def update(self, time, frame_time):
        self.App.set_uniform(self.displayAnts_prog, "frame_time", frame_time)
        if not self.isPheromoneWar:
            self.updateWeatheringRedistribution(frame_time)

        self.fbo.use()

        self.App.ctx.point_size = self.pointSize
        self.ants.render(self.displayAnts_prog)
        if not self.isPheromoneWar:
            self.fullScreen.render(self.pheromoneUpdate_prog)

        self.App.mainFbo.use()

    def render(self):
        if self.isPheromoneWar:
            self.fullScreen.render(self.pheromoneWar_prog)

    @staticmethod
    def initPheromoneTextureInGLSL():
        with open("resources/shaders/ants/__pheromone_textures__.glsl", "w") as pheromone_textures:
            for pheromone in Pheromone.pheromones:
                pheromone_textures.write(f"uniform sampler2D {pheromone.name};\n")
            pheromone_textures.write("\n")

            pheromone_textures.write("vec2 getPheromone(float id, vec2 uv) {\n"
                                     "    vec2 result = vec2(0.);\n")
            for i, pheromone in enumerate(Pheromone.pheromones):
                if not i:
                    pheromone_textures.write(f"    if (int(id) == {i}) ""{\n")
                elif i != len(Pheromone.pheromones) - 1:
                    pheromone_textures.write("    }"f" else if (int(id) == {i}) ""{\n")
                else:
                    pheromone_textures.write("    } else {\n")
                pheromone_textures.write(f"            result = (texture({pheromone.name},"
                                         f" uv).rg - 0.5) * 2;\n")
            pheromone_textures.write("    }\n"
                                     "    return result;\n"
                                     "}\n")
