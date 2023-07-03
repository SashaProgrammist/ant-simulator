from moderngl_window import geometry


class MappTexturesInfo:
    def __init__(self, name, texture, index):
        self.name = name
        self.texture = texture
        self.index = index


class Mapp:
    def __init__(self, App):
        self.App = App
        self.countTextures = 0

        self.quad = geometry.quad_fs(self.App.attributeNames)

        self.textures: dict[str, MappTexturesInfo] = {}
        self.addTexture("mappTexture", self.App.load_texture_2d("../mapp/mapp.png"))

        self.prog = self.App.load_program(
            vertex_shader='mapp_vertex_shader.glsl',
            fragment_shader='mapp_fragment_shader.glsl')
        self.set_uniformTextures(self.prog, "mappTexture")

    def addTexture(self, name, texture):
        self.textures[name] = MappTexturesInfo(name, texture, self.countTextures)
        texture.use(location=self.textures[name].index)

        self.countTextures += 1

    def set_uniformTextures(self, prog, name):
        self.App.set_uniform(prog, name, self.textures[name].index)

    def set_newResolution(self):
        self.App.set_uniform(self.prog, "resolution", self.App.window_size)

    def render(self):
        self.quad.render(self.prog)
