from moderngl_window import geometry
import moderngl as mgl


class MappTexturesInfo:
    def __init__(self, App, name, texture, index):
        self.App = App
        self.name = name
        self.texture = texture
        self.index = index
        self._fbo: mgl.Framebuffer = None

    @property
    def fbo(self):
        if self._fbo is None:
            self._fbo = self.App.ctx.framebuffer(self.texture)
        return self._fbo


class Mapp:
    countTextures = 0

    mappTexture = "mappTexture"
    mappDirection = "mappDirection"

    def __init__(self, App):
        self.App = App

        self.quad = self.App.fullScreen

        self.textures: dict[str, MappTexturesInfo] = {}
        self.addTexture(Mapp.mappTexture, self.App.load_texture_2d("mapp/mapp.png"))
        self.addTexture(Mapp.mappDirection, self.App.ctx.texture(self.App.window_size, 2), )

        self.simple_prog = self.App.load_program(
            vertex_shader='shaders/mapp/mapp_simple_vertex_shader.glsl',
            fragment_shader='shaders/mapp/mapp_simple_fragment_shader.glsl')
        self.set_uniformTextures(self.simple_prog, Mapp.mappTexture)

        self.mappDirection_prog = self.App.load_program(
            vertex_shader='shaders/mapp/mapp_direction_vertex_shader.glsl',
            fragment_shader='shaders/mapp/mapp_direction_fragment_shader.glsl')
        self.set_uniformTextures(self.mappDirection_prog, Mapp.mappTexture)

        self.putAwayFood_prog = self.App.load_program(
            vertex_shader='shaders/mapp/putAwayFood_vertex_shader.glsl',
            fragment_shader='shaders/mapp/putAwayFood_fragment_shader.glsl')
        self.set_uniformTextures(self.putAwayFood_prog, Mapp.mappTexture)

        self.applyChangeMappTexture()

    def applyChangeMappTexture(self):
        self.textures[Mapp.mappDirection].fbo.use()
        self.quad.render(self.mappDirection_prog)
        self.App.mainFbo.use()

    def addTexture(self, name, texture):
        self.textures[name] = MappTexturesInfo(self.App, name, texture, Mapp.countTextures)
        texture.use(location=self.textures[name].index)

        Mapp.countTextures += 1

    def set_uniformTextures(self, prog, name):
        self.App.set_uniform(prog, name, self.textures[name].index)

    def set_newResolution(self):
        self.App.set_uniform(self.simple_prog, "resolution", self.App.window_size)

    def render(self):
        self.quad.render(self.simple_prog)

    def update(self, time, frame_time):
        self.App.set_uniform(self.putAwayFood_prog,
                             "time", time)
        self.App.set_uniform(self.putAwayFood_prog,
                             "frame_time", frame_time)

        self.textures[Mapp.mappTexture].fbo.use()
        self.App.ctx.point_size = 3
        self.App.ants.ants.render(self.putAwayFood_prog)
        self.App.mainFbo.use()
