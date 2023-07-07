from moderngl_window.context.base.window import logger
import numpy as np
import os
import shutil
import cv2


def delFolder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


class SaveAnimation:
    self = None
    oldClose = None

    def __init__(self, App, countFrame, name,
                 fps, fpsSim, invisibleFrames, isSaveSequence):
        self.App = App
        self.countFrame = countFrame
        self.fps = fps
        self.fpsSim = fpsSim
        self.framesSim = invisibleFrames + 1
        self.isSaveSequence = isSaveSequence

        if self.isSaveSequence:
            delFolder("animation/animationTemp")

        self.indexFrame = 0
        self.indexSimFrame = 0
        self.video = cv2.VideoWriter(
            f'animation/saveAnimation/{name}.avi',
            cv2.VideoWriter_fourcc(*'mp4v'), self.fps,
            self.App.window_size)
        self.App.video = self.video
        self.ctx = self.App.ctx

        self.textureFbo = self.ctx.texture(self.App.window_size, 4, dtype="f1")
        self.textureFboId = self.App.countTextures
        self.App.countTextures += 1
        self.textureFbo.use(location=self.textureFboId)

        self.textureConvert = self.ctx.texture(self.App.window_size, 4)
        self.Convert = self.ctx.framebuffer(self.textureConvert)
        self.prog = self.ctx.program(
            vertex_shader="#version 400\n"
                          "in vec3 in_position;\n"
                          "in vec2 in_texCoord;\n"
                          "out vec2 v_texCoord;\n"
                          "void main() {\n"
                          "    gl_Position = vec4(in_position, 1);\n"
                          "    v_texCoord = in_texCoord;\n"
                          "}\n",
            fragment_shader="#version 400\n"
                            "in vec2 v_texCoord;\n"
                            "uniform sampler2D _textureFbo;\n"
                            "out vec4 fragColor;\n"
                            "void main() {\n"
                            "    fragColor = "
                            "vec4(texture(_textureFbo, v_texCoord * vec2(1, -1)).bgr, 1);\n"
                            "}\n")
        self.prog["_textureFbo"] = self.textureFboId

        SaveAnimation.self = self

    def callOldClose(self):
        oldClose = SaveAnimation.oldClose
        oldClose(self.App)

    def render(self):
        time, frameTime = self.indexSimFrame / self.fpsSim, 1 / self.fpsSim
        self.ctx.clear()
        for i in range(self.framesSim):
            self.App.update(time, frameTime)
            self.indexSimFrame += 1
            time = self.indexSimFrame / self.fpsSim

        self.App.renderVao()

        self.textureFbo.write(self.App.mainFbo.read(components=4))
        self.Convert.use()
        self.App.fullScreen.render(self.prog)
        self.App.mainFbo.use()

        raw = self.Convert.read(components=3, dtype='f1')
        buf: np.ndarray = np.frombuffer(raw, dtype='uint8'). \
            reshape((*self.App.mainFbo.size[1::-1], 3))

        if self.isSaveSequence:
            path = f"animation/animationTemp/" + \
                   '0' * (len(str(self.countFrame // self.framesSim)) -
                          len(str(self.indexFrame))) + \
                   f"{self.indexFrame}.png"
            cv2.imwrite(path, buf)

        self.video.write(buf)

        if self.countFrame is not None and self.indexFrame >= self.countFrame:
            self.App.wnd.is_closing = True

            self.video.release()

            self.App.close()

        self.indexFrame += 1

    def close(self):
        self.callOldClose()

        self.video.release()
        unitTimes = [60, 60, 24, 30, 12]
        unitTimesNames = ["m", "h", "d", "m", "e"]
        i = 0
        time = self.App.timer.time
        timeSim = self.indexSimFrame / self.fpsSim
        unitTime = "s"
        while i < len(unitTimes) and timeSim >= unitTimes[i]:
            timeSim /= unitTimes[i]
            unitTime = unitTimesNames[i]
            i += 1
        logger.info(f"time in sim: {timeSim:.2f} {unitTime} @ "
                    f"{self.indexFrame / time * self.framesSim:.2f} ups")

    @staticmethod
    def getNew__init__(cls, countFrame, name, fps,
                       fpsSim, invisibleFrames, isSaveSequence):
        old__init__ = cls.__init__

        def new__init__(_self, **kwargs):
            old__init__(_self, **kwargs)

            _self.saveAnimation = SaveAnimation(
                _self, countFrame, name, fps,
                fpsSim, invisibleFrames, isSaveSequence)

        return new__init__

    @staticmethod
    def getNewClose(*_):
        return SaveAnimation.self.oldClose()

    @staticmethod
    def getNewRender(*_):
        return SaveAnimation.self.render()
