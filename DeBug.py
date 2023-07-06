
class DeBug:
    def __init__(self, App):
        self.App = App
        self.deBag_prog = self.App.load_program(
            vertex_shader='shaders/deBag/deBag_vertex_shader.glsl',
            fragment_shader='shaders/deBag/deBag_fragment_shader.glsl')

        self.isRender = False
        self.isRenderAnt = True

    def render(self):
        pass
