import moderngl_window as mglw
import numpy as np
from itertools import chain


class DeBug:
    SHIFT = 65505
    CTRL = 65507

    def __init__(self, App: mglw.WindowConfig):
        self.App = App
        self.deBag_prog = self.App.load_program(
            vertex_shader='shaders/deBag/deBag_vertex_shader.glsl',
            fragment_shader='shaders/deBag/deBag_fragment_shader.glsl')

        self.isRender = False
        self.isRenderAnt = True

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
    def number0(self):
        return self.App.wnd.keys.NUMBER_0

    @property
    def number9(self):
        return self.App.wnd.keys.NUMBER_9

    def addInCollectorCtrl(self, letter):
        if len(self.collectorCtrl) >= 3:
            self.collectorCtrl = self.collectorCtrl[-2:] + letter
        else:
            self.collectorCtrl += letter

    def key_event(self, key, action, *_):
        if action == self.App.wnd.keys.ACTION_PRESS:
            match key:
                case self.SHIFT:
                    self.isShift = True
                case self.A:
                    self.isRenderAnt = not self.isRenderAnt
                case self.CTRL:
                    self.isCtrl = True

            if self.isShift and key in self.numbersKeys:
                self.collectorShift += self.numbersKeys[key]

            if self.isCtrl and key in self.colorKeys:
                self.addInCollectorCtrl(self.colorKeys[key])
        else:
            match key:
                case self.SHIFT:
                    print(self.collectorShift)
                    self.collectorShift = ""
                    self.isShift = False
                case self.CTRL:
                    print(self.collectorCtrl)
                    self.collectorCtrl = ""
                    self.isCtrl = False

    def render(self):
        pass
