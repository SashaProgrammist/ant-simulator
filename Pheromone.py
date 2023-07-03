import moderngl as mgl
import moderngl_window as mglw
from moderngl_window import geometry
from moderngl_window.opengl.vao import VAO, BufferInfo


class Pheromone:
    countPheromone = 0

    def __init__(self, App, pointSize=None, name=None, isPheromoneWar=False,
                 weathering=0.9, redistribution=0.1):
        Pheromone.countPheromone += 1

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
            self.name = f"pheromone {Pheromone.countPheromone}"
        self.isPheromoneWar = isPheromoneWar
        self.weathering = weathering - redistribution
        self.redistribution = redistribution / 8

        self.texture = self.App.ctx.texture(self.App.window_size, 3)
        self.texture.use(Pheromone.countPheromone)

        self.fbo = self.App.ctx.simple_framebuffer(self.App.window_size)

        self.ants = VAO(self.name, mode=mgl.POINTS)
        buffers: list[tuple[BufferInfo, str]] = self.App.ants.buffers
        for buffer in buffers:
            self.ants.buffer(buffer[0].buffer, buffer[1], buffer[0].attributes)

        self.fullScreen = geometry.quad_fs(self.App.attributeNames)

        self.displayAnts_prog = self.App.load_program(
            vertex_shader="pheromone_display_ants_vertex_shader.glsl",
            fragment_shader="pheromone_display_ants_fragment_shader.glsl")
        self.App.set_uniform(self.displayAnts_prog, "isPheromoneWar", self.isPheromoneWar)
        self.App.set_uniform(self.displayAnts_prog, "pheromone", Pheromone.countPheromone - 1)

        if not self.isPheromoneWar:
            self.pheromoneUpdate_prog = self.App.load_program(
                vertex_shader="pheromone_update_vertex_shader.glsl",
                fragment_shader="pheromone_update_fragment_shader.glsl")
            self.App.set_uniform(self.pheromoneUpdate_prog, "mappTexture",
                                 self.App.mappTextureID)
            self.App.set_uniform(self.pheromoneUpdate_prog, "pheromoneTexture",
                                 Pheromone.countPheromone)
            self.App.set_uniform(self.pheromoneUpdate_prog, "weathering",
                                 self.weathering)
            self.App.set_uniform(self.pheromoneUpdate_prog, "redistribution",
                                 self.redistribution)
        else:
            self.pheromoneUpdate_prog = None

    def set_newResolution(self):
        self.App.set_uniform(self.displayAnts_prog, "resolution", self.App.window_size)
        if not self.isPheromoneWar:
            self.App.set_uniform(self.pheromoneUpdate_prog, "resolution", self.App.window_size)

    def update(self):
        pass
        self.texture.write(self.fbo.read())

    def render(self):
        self.fbo.use()

        if not self.isPheromoneWar:
            self.fullScreen.render(self.pheromoneUpdate_prog)
        self.App.ctx.point_size = self.pointSize
        self.ants.render(self.displayAnts_prog)

        self.App.ctx.fbo.use()
