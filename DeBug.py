import moderngl_window as mglw
from moderngl_window.context.base.window import logger
from itertools import chain
import numpy as np


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
            self.App.wnd.keys.SPACE: "_",
            65454: '.',  # numpad
            47: '.',  # English layout
            816043786240: '.'}  # Russian layout
        self.numpadNumbers = [
            65379,       65367, 65364, 65366, 65361,
            51539607552, 65363, 65360, 65362, 65365]
        self.numbersKeys = {
            keys: str(i) for i, keys in
            chain(enumerate(range(self.number0, self.number9 + 1)),
                  enumerate(self.numpadNumbers),
                  enumerate(range(self.numpad0, self.numpad9 + 1)))}
        pass

    @property
    def A(self):
        return self.App.wnd.keys.A

    @property
    def W(self):
        return self.App.wnd.keys.W

    @property
    def S(self):
        return self.App.wnd.keys.S

    @property
    def number0(self):
        return self.App.wnd.keys.NUMBER_0

    @property
    def number9(self):
        return self.App.wnd.keys.NUMBER_9

    @property
    def numpad0(self):
        return self.App.wnd.keys.NUMPAD_0

    @property
    def numpad9(self):
        return self.App.wnd.keys.NUMPAD_9

    @property
    def actionPress(self):
        return self.App.wnd.keys.ACTION_PRESS

    def setChannels(self, code: str):
        countPoint = code.count('.')
        if countPoint < 2:
            code = code.replace('.', '_')
            newCode = ''
            for letter in code:
                if letter.isalpha():
                    newCode += letter
            code = newCode
        elif countPoint > 2:
            code = '.'.join(code.split('.')[-3:])

        shortCodes = {
            '': "rgb", 'r': "r__", 'g': "_g_", 'b': "__b",
            'rr': "r__", 'gg': "_g_", 'bb': "__b",
            'rb': "r_b", 'br': "r_b", 'rg': "r_g",
            'gr': "r_g", 'bg': "_bg", 'gb': "_bg"}

        if len(code) < 3:
            code = code.replace('_', '')
            code = shortCodes[code]

        if len(code) > 3 and countPoint < 2:
            code = code[-3:]

        if len(code) == 3 and countPoint < 2:
            code = '.'.join(code)

        code = code.replace('_', '')

        channels: dict[str, np.ndarray] = {
            'r': np.array(np.zeros(3), dtype=np.float32),
            'g': np.array(np.zeros(3), dtype=np.float32),
            'b': np.array(np.zeros(3), dtype=np.float32)}
        for i, resultChanel in enumerate(code.split('.')):
            for j, letter in enumerate(resultChanel):
                if letter.isalpha():
                    number = ''
                    current = j + 1
                    while current < len(resultChanel) and resultChanel[current].isdigit():
                        number += resultChanel[current]
                        current += 1
                    if not number:
                        number = 1
                    channels[letter][i] += int(number)

        sums = [0, 0, 0]
        for channel in channels.values():
            for i, value in enumerate(channel):
                sums[i] += value

        for channel in channels.values():
            for i in range(3):
                if sums[i]:
                    channel[i] /= sums[i]

        logger.info(f"setChannels: \n{channels}")

        for channel, value in channels.items():
            self.App.set_uniform(self.prog, f"channel{channel.upper()}",
                                 value)

    def setStandardChannels(self):
        self.setChannels("rgb")

    def setChannelsFromCollector(self):
        if self.isRender:
            self.setChannels(self.collectorCtrl)
        self.collectorCtrl = ''
        self.isCtrl = False

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
                case self.S:
                    if self.isCtrl:
                        if self.collectorCtrl.count('.'):
                            self.collectorCtrl = self.collectorCtrl.split('.')[-1]
                        self.collectorCtrl = '.'.join([self.collectorCtrl] * 3)
                        self.setChannelsFromCollector()

            if self.isShift and key in self.numbersKeys:
                self.collectorShift += self.numbersKeys[key]

            if self.isCtrl and key in self.colorKeys:
                self.collectorCtrl += self.colorKeys[key]
            if self.isCtrl and not self.isShift and key in self.numbersKeys:
                self.collectorCtrl += self.numbersKeys[key]
        else:
            match key:
                case self.SHIFT:
                    if self.collectorShift:
                        self.App.set_uniform(self.prog, "_texture",
                                             int(self.collectorShift))
                        self.isRender = True
                        self.setChannels(self.collectorCtrl)
                    else:
                        self.isRender = False
                        self.setStandardChannels()
                    self.collectorShift = ""
                    self.isShift = False
                case self.CTRL:
                    if self.isCtrl:
                        self.setChannelsFromCollector()

    def render(self):
        if self.isRender:
            self.App.fullScreen.render(self.prog)
