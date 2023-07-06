import moderngl_window as mglw
from itertools import chain


class DeBug:
    SHIFT = 65505
    CTRL = 65507

    def __init__(self, App: mglw.WindowConfig):
        self.App = App
        self.prog = self.App.load_program(
            vertex_shader='shaders/deBag/deBag_vertex_shader.glsl',
            fragment_shader='shaders/deBag/deBag_fragment_shader.glsl')
        self.setStandardChannels()

        self.isRender = False
        self.isRenderAnt = True
        self.isRenderPheromoneWar = True

        self.isCtrl = False
        self.isShift = False

        self.collectorCtrl = ""
        self.collectorShift = ""

        self.colorKeys = {
            self.App.wnd.keys.R: "r",
            self.App.wnd.keys.G: "g",
            self.App.wnd.keys.B: "b",
            self.App.wnd.keys.SPACE: "_"}
        self.numpadNumbers = [
            65379,       65367, 65364, 65366, 65361,
            51539607552, 65363, 65360, 65362, 65365]
        self.numbersKeys = {
            keys: str(i) for i, keys in
            chain(enumerate(range(self.number0, self.number9 + 1)),
                  enumerate(self.numpadNumbers))}
        pass

    @property
    def A(self):
        return self.App.wnd.keys.A

    @property
    def W(self):
        return self.App.wnd.keys.W

    @property
    def number0(self):
        return self.App.wnd.keys.NUMBER_0

    @property
    def number9(self):
        return self.App.wnd.keys.NUMBER_9

    @property
    def actionPress(self):
        return self.App.wnd.keys.ACTION_PRESS

    def setChannels(self, code: str):
        shortCodes = {
            '': "rgb", 'r': "r__", 'g': "_g_", 'b': "__b",
            'rb': "r_b", 'br': "r_b", 'rg': "r_g",
            'gr': "r_g", 'bg': "_bg", 'gb': "_bg"}

        if len(code) < 3:
            code.replace('_', '')
            code = shortCodes[code]

        channels: dict[str, list[int]] = {
            'r': [0, 0, 0],
            'g': [0, 0, 0],
            'b': [0, 0, 0],
            '_': [0, 0, 0]}
        for i, letter in enumerate(code):
            channels[letter][i] = 1

        for channel, value in channels.items():
            if channel != '_':
                self.App.set_uniform(self.prog, f"channel{channel.upper()}",
                                     tuple(value))

    def setStandardChannels(self):
        self.setChannels("rgb")

    def addInCollectorCtrl(self, letter):
        if len(self.collectorCtrl) >= 3:
            self.collectorCtrl = self.collectorCtrl[-2:] + letter
        else:
            self.collectorCtrl += letter

    def key_event(self, key, action, *_):
        if action == self.actionPress:
            match key:
                case self.SHIFT:
                    self.isShift = True
                case self.A:
                    self.isRenderAnt = not self.isRenderAnt
                case self.W:
                    self.isRenderPheromoneWar = not self.isRenderPheromoneWar
                case self.CTRL:
                    self.isCtrl = True

            if self.isShift and key in self.numbersKeys:
                self.collectorShift += self.numbersKeys[key]

            if self.isCtrl and key in self.colorKeys:
                self.addInCollectorCtrl(self.colorKeys[key])
        else:
            match key:
                case self.SHIFT:
                    if self.collectorShift:
                        self.App.set_uniform(self.prog, "_texture",
                                             int(self.collectorShift))
                        self.isRender = True
                    else:
                        self.isRender = False
                        self.setStandardChannels()
                    self.collectorShift = ""
                    self.isShift = False
                case self.CTRL:
                    if self.isRender:
                        self.setChannels(self.collectorCtrl)
                    self.collectorCtrl = ""
                    self.isCtrl = False

    def render(self):
        if self.isRender:
            self.App.fullScreen.render(self.prog)
