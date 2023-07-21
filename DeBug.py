import moderngl_window as mglw
from moderngl_window.context.base.window import logger
from itertools import chain
import numpy as np


class CtrlMode:
    def __init__(self, deBug, name, finalizer):
        self.deBug: DeBug = deBug
        self.name: str = name
        self._finalizer: callable = finalizer

    def __eq__(self, other):
        return self.name == other.name

    def finalizer(self):
        # _finalizer = self._finalizer
        # _finalizer()
        self._finalizer()
        self.deBug.currentCtrlMode = self.deBug.defaultCtrlMode


class PosibleToSet:
    channels = "channels"
    isRenderAnt = "isRenderAnt"
    isRenderPheromoneWar = "isRenderPheromoneWar"
    alfa = "alfa"
    texture = "texture"


class DeBug:
    SHIFT = 65505
    CTRL = 65507

    def __init__(self, App: mglw.WindowConfig):
        self.App = App

        self.possibleToSet = []

        self.prog = self.App.load_program(
            vertex_shader='shaders/deBag/deBag_vertex_shader.glsl',
            fragment_shader='shaders/deBag/deBag_fragment_shader.glsl')
        self.possibleToSet.append(PosibleToSet.texture)
        self.setStandardChannels()
        self.setStandardAlfa()

        self.isRender = False
        self.isRenderAnt = True
        self.possibleToSet.append(PosibleToSet.isRenderAnt)
        self.isRenderPheromoneWar = True
        self.possibleToSet.append(PosibleToSet.isRenderPheromoneWar)

        self.isCtrl = False
        self.isShift = False

        self.defaultCtrlMode = CtrlMode(self, "default",
                                        self.resetCollectorCtrl)
        self.colorCtrlMode = CtrlMode(self, PosibleToSet.channels,
                                      self.setChannelsFromCollector)
        self.possibleToSet.append(PosibleToSet.channels)
        self.alfaCtrlMode = CtrlMode(self, PosibleToSet.alfa,
                                     self.setAlfaFromCollector)
        self.possibleToSet.append(PosibleToSet.alfa)
        self.currentCtrlMode = self.defaultCtrlMode

        self.collectorCtrl = ""
        self.collectorShift = ""

        self.ctrlKeys = {
            self.App.wnd.keys.R: "r",
            self.App.wnd.keys.G: "g",
            self.App.wnd.keys.B: "b",
            self.App.wnd.keys.SPACE: "_",
            47: '.',  # English layout
            65454: '.',  # numpad
            816043786240: '.',  # Russian layout
            self.App.wnd.keys.SLASH: '/',  # English layout
            65455: '/',  # numpad
            92: '/'}  # Russian layout
        self.numpadCtrlNumbers = [  # numpad numbers when the control is pressed
            65379,       65367, 65364, 65366, 65361,
            51539607552, 65363, 65360, 65362, 65365]
        self.numbersKeys = {
            keys: str(i) for i, keys in
            chain(enumerate(range(self.number0, self.number9 + 1)),
                  enumerate(self.numpadCtrlNumbers),
                  enumerate(range(self.numpad0, self.numpad9 + 1)))}

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
    def C(self):
        return self.App.wnd.keys.C

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

    def set(self, **kwargs):
        for atr in kwargs:
            if atr in self.possibleToSet:
                if hasattr(self, atr):
                    setattr(self, atr, kwargs[atr])
            else:
                raise Exception(f"{atr} = {kwargs[atr]} is not possible to set")

        if PosibleToSet.texture in kwargs:
            self.setTexture(kwargs[PosibleToSet.texture])

        if PosibleToSet.channels in kwargs:
            self.setChannels(kwargs[PosibleToSet.channels])

        if PosibleToSet.alfa in kwargs:
            self.setAlfa(kwargs[PosibleToSet.alfa])

    @staticmethod
    def strCodeToFloat(code: str):
        code = DeBug.leaveLastsBlock(code, 2)

        countPoint = code.count('.')
        numerator, *denominators = code.split('/')

        if numerator.count('.') != countPoint:
            logger.exception("incorrect input")
            return

        number = float(numerator or '1')
        for denominator in denominators:
            number /= int(denominator)

        return number

    def setAlfa(self, code: str | float | int):
        if isinstance(code, str):
            number = self.strCodeToFloat(code)
        else:
            number = float(code)

        logger.info(f"setAlfa: {number}")

        self.App.set_uniform(self.prog, "alfa", number)

    @staticmethod
    def strCodeToNdarray(code: str):
        code = code.replace('/', '_')

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
                    while current < len(resultChanel) and \
                            resultChanel[current].isdigit():
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

        return np.array([channels['r'], channels['g'], channels['b']])

    def setChannels(self, code: str | np.ndarray):
        if isinstance(code, str):
            code = self.strCodeToNdarray(code)

        channels = dict()

        if not isinstance(code, np.ndarray):
            logger.error(f"wrong code class {code.__class__}")
            return

        if code.shape == (3,):
            for i, channel in zip(range(3), ('R', 'G', 'B')):
                zeros = np.zeros(3)
                zeros[i] = code[i]
                channels[channel] = zeros
                self.App.set_uniform(self.prog, f"channel{channel}",
                                     zeros)
        elif code.shape == (3, 3):
            for i, channel in zip(range(3), ('R', 'G', 'B')):
                channels[channel] = code[i]
                self.App.set_uniform(self.prog, f"channel{channel}",
                                     code[i])
        else:
            logger.error(f"wrong shape code {code}")

        logger.info(f"setChannels: \n{channels}")

    def setStandardChannels(self):
        self.setChannels("rgb")

    def setStandardAlfa(self):
        self.setAlfa("1")

    def setChannelsFromCollector(self):
        if self.isRender:
            self.setChannels(self.collectorCtrl)
        self.collectorCtrl = ''
        self.isCtrl = False

    def setAlfaFromCollector(self):
        if self.isRender:
            self.setAlfa(self.collectorCtrl)
        self.collectorCtrl = ''
        self.isCtrl = False

    def setTexture(self, newId):
        self.App.set_uniform(self.prog, "_texture",
                             newId)
        self.isRender = True
        self.setStandardChannels()
        self.setStandardAlfa()

    def resetCollectorCtrl(self):
        self.collectorCtrl = ''

    @staticmethod
    def leaveLastsBlock(code, countBlock=1):
        if code.count('.') >= countBlock:
            return '.'.join(code.split('.')[-countBlock:])
        return code

    def key_event(self, key, action, *_):
        if action == self.actionPress:
            match key:
                case self.SHIFT:
                    self.isShift = True
                case self.A:
                    if not self.isCtrl:
                        self.isRenderAnt = not self.isRenderAnt
                    else:
                        self.currentCtrlMode = self.alfaCtrlMode
                case self.W:
                    self.isRenderPheromoneWar = not self.isRenderPheromoneWar
                case self.C:
                    if self.isCtrl:
                        self.currentCtrlMode = self.colorCtrlMode
                case self.CTRL:
                    self.isCtrl = True
                case self.S:
                    if self.isCtrl and self.currentCtrlMode == self.colorCtrlMode:
                        self.collectorCtrl = self.leaveLastsBlock(self.collectorCtrl)
                        self.collectorCtrl = '.'.join([self.collectorCtrl] * 3)
                        self.currentCtrlMode.finalizer()

            if self.isShift and key in self.numbersKeys:
                self.collectorShift += self.numbersKeys[key]

            if self.isCtrl and key in self.ctrlKeys:
                self.collectorCtrl += self.ctrlKeys[key]
            if self.isCtrl and not self.isShift and key in self.numbersKeys:
                self.collectorCtrl += self.numbersKeys[key]
        else:
            match key:
                case self.SHIFT:
                    if self.collectorShift:
                        self.setTexture(int(self.collectorShift))
                    else:
                        self.isRender = False
                        self.setStandardChannels()
                    self.collectorShift = ""
                    self.isShift = False
                case self.CTRL:
                    if self.isCtrl:
                        self.currentCtrlMode.finalizer()

    def render(self):
        if self.isRender:
            self.App.fullScreen.render(self.prog)
