import numpy as np

from DeBug import DeBug, PosibleToSet


class KeyFrame:
    def __init__(self, frameIndex, kwargs):
        self.frameIndex = frameIndex
        self.kwargs: dict = kwargs

        if PosibleToSet.channels in self.kwargs and \
                isinstance(self.kwargs[PosibleToSet.channels], str):
            self.kwargs[PosibleToSet.channels] = \
                DeBug.strCodeToNdarray(self.kwargs[PosibleToSet.channels])

        if PosibleToSet.alfa in self.kwargs:
            alfa = self.kwargs[PosibleToSet.alfa]
            if isinstance(alfa, str):
                self.kwargs[PosibleToSet.alfa] = \
                    DeBug.strCodeToFloat(alfa)
            elif isinstance(alfa, int):
                self.kwargs[PosibleToSet.alfa] = float(alfa)

    def __repr__(self):
        return f"(frameIndex = {self.frameIndex}, kwargs =\n{self.kwargs})"


class Interpolator:
    def __init__(self, chang, keyFrames, countFrame,
                 interpolationFunction):
        self.chang = chang
        self.keyFrames: list[KeyFrame] = keyFrames
        self.countFrame = countFrame

        self.revers = dict()
        for keyFrame in self.keyFrames:
            self.revers[keyFrame.frameIndex] = keyFrame

        self.currentKey = np.zeros(self.countFrame, dtype=int)
        for keyFrame in self.keyFrames:
            if chang in keyFrame.kwargs:
                self.currentKey[keyFrame.frameIndex] = keyFrame.frameIndex

        for i in range(1, self.countFrame):
            if not self.currentKey[i]:
                self.currentKey[i] = self.currentKey[i - 1]

        self.isInter = isinstance(
            self.keyFrames[0].kwargs[self.chang],
            (np.ndarray, float))

        if self.isInter:
            self.interFunc = interpolationFunction
            self.nextKey = np.zeros(self.countFrame, dtype=int)

            for keyFrame in self.keyFrames:
                if chang in keyFrame.kwargs:
                    self.nextKey[keyFrame.frameIndex] = keyFrame.frameIndex

            for i in range(2, self.countFrame):
                if not self.nextKey[-i]:
                    self.nextKey[-i] = self.nextKey[1 - i]

    def interpolate(self, indexFrame):
        if self.isInter:
            current = self.currentKey[indexFrame]
            _next = self.nextKey[indexFrame]

            if current == _next:
                return self.revers[current].kwargs[self.chang]

            alfa = self.interFunc((indexFrame - current) / (_next - current))

            return \
                self.revers[current].kwargs[self.chang] * (1 - alfa) + \
                self.revers[_next].kwargs[self.chang] * alfa

        return self.revers[self.currentKey[indexFrame]].kwargs[self.chang]


class KeyFrameManager:
    def __init__(self, interpolationFunction=lambda x: x * x * (3 - 2 * x)):
        self.saveAnimation = None
        self.App = None
        self.interFunc = interpolationFunction

        self.keyFrames: list[KeyFrame] = []
        self.interpolators: dict[str, Interpolator] = dict()

    def addKeyFrame(self, frameIndex, **kwargs):
        self.keyFrames.append(KeyFrame(frameIndex, kwargs))

    def set(self, saveAnimation, App):
        self.saveAnimation = saveAnimation
        self.App = App

        if self.saveAnimation.countFrame is None:
            raise Exception("countFrame must be defined")

    def setFrame(self):
        self.App.deBug.set(**{
            chang: interpolator.interpolate(self.saveAnimation.indexFrame)
            for chang, interpolator in self.interpolators.items()
        })

    def build(self):
        self.keyFrames.sort(key=lambda _keyFrame: _keyFrame.frameIndex)

        changeable = set()
        for keyFrame in self.keyFrames:
            changeable = changeable.union(set(keyFrame.kwargs))

        if self.keyFrames:
            if self.keyFrames[0].frameIndex != 0:
                first = KeyFrame(0, {chang: None for chang in changeable})
                self.keyFrames.insert(0, first)
            else:
                for chang in changeable:
                    if chang not in self.keyFrames[0].kwargs:
                        self.keyFrames[0].kwargs[chang] = None
            i = 0
            while any(map(lambda var: var is None, self.keyFrames[0].kwargs.values())):
                for chang in self.keyFrames[i].kwargs:
                    if self.keyFrames[0].kwargs[chang] is None:
                        self.keyFrames[0].kwargs[chang] = self.keyFrames[i].kwargs[chang]
                i += 1

        countFrame = self.saveAnimation.countFrame

        if self.keyFrames:
            if self.keyFrames[-1].frameIndex != countFrame - 1:
                end = KeyFrame(countFrame - 1, {chang: None for chang in changeable})
                self.keyFrames.append(end)
            else:
                for chang in changeable:
                    if chang not in self.keyFrames[-1].kwargs:
                        self.keyFrames[-1].kwargs[chang] = None
            i = -1
            while any(map(lambda var: var is None, self.keyFrames[-1].kwargs.values())):
                for chang in self.keyFrames[i].kwargs:
                    if self.keyFrames[-1].kwargs[chang] is None:
                        self.keyFrames[-1].kwargs[chang] = self.keyFrames[i].kwargs[chang]

                i -= 1

        for chang in changeable:
            self.interpolators[chang] = \
                Interpolator(chang, self.keyFrames, countFrame,
                             self.interFunc)
