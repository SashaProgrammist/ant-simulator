import moderngl as mgl
import moderngl_window as mglw
from moderngl_window.opengl.vao import VAO, BufferInfo


class Pheromone:
    countPheromone = 0

    def __init__(self, App, pointSize=5, name=None, isPheromoneWar=False):
        Pheromone.countPheromone += 1

        self.App = App
        self.pointSize = pointSize
        if name is not None:
            self.name = name
        else:
            self.name = f"pheromone {Pheromone.countPheromone}"
        self.isPheromoneWar = isPheromoneWar

        self.texture = self.App.ctx.texture(self.App.window_size, 3)
        self.texture.use(Pheromone.countPheromone)

        self.fbo = self.App.ctx.simple_framebuffer(self.App.window_size)

        self.vao = VAO(self.name, mode=mgl.POINTS)
        buffers: list[tuple[BufferInfo, str]] = self.App.ants.buffers
        for buffer in buffers:
            self.vao.buffer(buffer[0].buffer, buffer[1], buffer[0].attributes)

        vertex_shader = open("shaders/pheromone_vertex_shader.glsl")
        fragment_shader = open("shaders/pheromone_fragment_shader.glsl")
        try:
            self.prog = self.App.ctx.program(
                vertex_shader=vertex_shader.read(),
                fragment_shader=fragment_shader.read()
            )
        finally:
            vertex_shader.close()
            fragment_shader.close()
        self.prog["isPheromoneWar"] = self.isPheromoneWar
        self.prog["pheromone"] = Pheromone.countPheromone - 1

    def update(self):
        pass
        self.texture.write(self.fbo.read())

    def render(self):
        self.fbo.use()

        self.App.ctx.point_size = self.pointSize
        self.vao.render(self.prog)

        self.App.ctx.fbo.use()
