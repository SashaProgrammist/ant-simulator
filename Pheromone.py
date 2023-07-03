import moderngl as mgl
import moderngl_window as mglw
from moderngl_window import geometry
from moderngl_window.opengl.vao import VAO

from Ants import AntBufferInfo
from Mapp import Mapp


class Pheromone:
    countPheromone = 0
    pheromones = []

    def __init__(self, App, pointSize=None, name=None, isPheromoneWar=False,
                 weathering=0.9, redistribution=0.1, redistributionRadius=10):
        self.App = App
        if pointSize is not None:
            self.pointSize = pointSize
        else:
            if isPheromoneWar:
                self.pointSize = 50
            else:
                self.pointSize = 5
        if name is not None:
            self.name = name
        else:
            self.name = f"pheromone_{Pheromone.countPheromone}"
        self.isPheromoneWar = isPheromoneWar
        self.weathering = weathering
        self.redistribution = redistribution
        self.redistributionRadius = redistributionRadius

        self.texture = self.App.ctx.texture(self.App.window_size, 2)
        self.texture.use(Pheromone.countPheromone + self.App.mapp.countTextures)

        self.fbo = self.App.ctx.framebuffer(self.texture)
        self.fbo.use()
        self.App.ctx.clear(0.5, 0.5)
        self.App.ctx.fbo.use()

        self.ants: VAO = VAO(self.name, mode=mgl.POINTS)

        self.fullScreen = geometry.quad_fs(self.App.attributeNames)

        self.displayAnts_prog = self.App.load_program(
            vertex_shader="pheromone_display_ants_vertex_shader.glsl",
            fragment_shader="pheromone_display_ants_fragment_shader.glsl")
        self.App.set_uniform(self.displayAnts_prog, "isPheromoneWar", self.isPheromoneWar)
        self.App.set_uniform(self.displayAnts_prog, "pheromone", Pheromone.countPheromone)

        if not self.isPheromoneWar:
            self.pheromoneUpdate_prog = self.App.load_program(
                vertex_shader="pheromone_update_vertex_shader.glsl",
                fragment_shader="pheromone_update_fragment_shader.glsl")
            self.App.mapp.set_uniformTextures(self.pheromoneUpdate_prog, Mapp.mappTexture)
            self.App.set_uniform(self.pheromoneUpdate_prog, "pheromoneTexture",
                                 Pheromone.countPheromone + self.App.mapp.countTextures)
            self.updateWeatheringRedistribution(1, 1)
            self.App.set_uniform(self.pheromoneUpdate_prog, "redistributionRadius",
                                 self.redistributionRadius)
        else:
            self.pheromoneUpdate_prog = None

        Pheromone.countPheromone += 1
        Pheromone.pheromones.append(self)

    def initAnts(self):
        buffers: list[AntBufferInfo] = self.App.ants.buffers
        for buffer in buffers:
            self.ants.buffer(buffer.buffer, buffer.buffer_format, buffer.attributes)

    def set_newResolution(self):
        self.App.set_uniform(self.displayAnts_prog, "resolution", self.App.window_size)
        if not self.isPheromoneWar:
            self.App.set_uniform(self.pheromoneUpdate_prog, "resolution", self.App.window_size)

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

    def render(self):
        self.fbo.use()

        if not self.isPheromoneWar:
            self.fullScreen.render(self.pheromoneUpdate_prog)
        self.App.ctx.point_size = self.pointSize
        self.ants.render(self.displayAnts_prog)

        self.App.ctx.fbo.use()

    @staticmethod
    def initPheromoneTextureInGLSL():
        with open("shaders/__pheromone_textures__.glsl", "w") as pheromone_textures:
            for pheromone in Pheromone.pheromones:
                pheromone_textures.write(f"uniform sampler2D {pheromone.name};\n")
            pheromone_textures.write("\n")

            pheromone_textures.write("sampler2D getPheromone(float id) {\n"
                                     "    switch (int(id)) {\n")
            for i, pheromone in enumerate(Pheromone.pheromones):
                if i != len(Pheromone.pheromones) - 1:
                    pheromone_textures.write(f"        case {i}:\n")
                else:
                    pheromone_textures.write(f"        default:\n")
                pheromone_textures.write(f"            return {pheromone.name};\n")
            pheromone_textures.write("    }\n"
                                     "}\n")
