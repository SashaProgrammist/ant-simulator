import moderngl_window as mglw
from PIL import Image, ImageDraw


class Pheromone:
    def __init__(self, App: mglw.WindowConfig):
        self.App = App

        self.image = Image.new("LA", self.App.window_size)
        self.imageDraw = ImageDraw.Draw(self.image)
        self.texture = self.App.ctx.texture(self.App.window_size, 1)

        self.texture.use(2)

    def update(self):
        self.texture.write(self.image.convert("L").tobytes())
