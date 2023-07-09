from App import *
from KeyFrameManager import KeyFrameManager
from DeBug import PosibleToSet

saveAnimation = True

if __name__ == '__main__':
    if saveAnimation:
        keyFrameManager = KeyFrameManager()

        keyFrameManager.addKeyFrame(100, **{
            PosibleToSet.alfa: 0,
            PosibleToSet.texture: 3})
        keyFrameManager.addKeyFrame(200, **{
            PosibleToSet.alfa: 1,
            PosibleToSet.isRenderAnt: True})
        keyFrameManager.addKeyFrame(300, **{
            PosibleToSet.isRenderAnt: False,
            PosibleToSet.channels: "rgb"})
        keyFrameManager.addKeyFrame(400, **{
            PosibleToSet.isRenderAnt: False,
            PosibleToSet.channels: "r.."})
        keyFrameManager.addKeyFrame(500, **{
            PosibleToSet.isRenderAnt: False,
            PosibleToSet.channels: "rgb"})
        keyFrameManager.addKeyFrame(600, **{
            PosibleToSet.isRenderAnt: False,
            PosibleToSet.channels: ".g."})
        keyFrameManager.addKeyFrame(700, **{
            PosibleToSet.isRenderAnt: False,
            PosibleToSet.channels: "rgb"})
        keyFrameManager.addKeyFrame(800, **{
            PosibleToSet.isRenderAnt: False,
            PosibleToSet.channels: "..b"})
        keyFrameManager.addKeyFrame(900, **{
            PosibleToSet.isRenderAnt: False,
            PosibleToSet.channels: "rgb"})

        App.saveAnimation(countFrame=1000, name="Test", isSaveSequence=False,
                          fps=24., fpsSim=60, invisibleFrames=4)

        SaveAnimation.setKeyFrameManager(keyFrameManager)

    mglw.run_window_config(App)
