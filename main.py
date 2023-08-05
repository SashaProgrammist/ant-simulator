from App import *
from KeyFrameManager import KeyFrameManager
from DeBug import PosibleToSet

saveAnimation = False

if __name__ == '__main__':
    if saveAnimation:
        keyFrameManager = KeyFrameManager()

        keyFrameManager.addKeyFrame(0, **{
            PosibleToSet.texture: 3})
        keyFrameManager.addKeyFrame(10, **{
            PosibleToSet.alfa: 0})
        keyFrameManager.addKeyFrame(20, **{
            PosibleToSet.alfa: 1,
            PosibleToSet.isRenderAnt: True})
        keyFrameManager.addKeyFrame(30, **{
            PosibleToSet.isRenderAnt: False,
            PosibleToSet.channels: "rgb"})
        keyFrameManager.addKeyFrame(40, **{
            PosibleToSet.channels: "r"})
        keyFrameManager.addKeyFrame(50, **{
            PosibleToSet.channels: "rgb"})
        keyFrameManager.addKeyFrame(60, **{
            PosibleToSet.channels: "g"})
        keyFrameManager.addKeyFrame(70, **{
            PosibleToSet.channels: "rgb"})
        keyFrameManager.addKeyFrame(80, **{
            PosibleToSet.channels: "b"})
        keyFrameManager.addKeyFrame(90, **{
            PosibleToSet.channels: "rgb"})

        App.saveAnimation(countFrame=100, name="Test", isSaveSequence=False,
                          fps=24., fpsSim=60, invisibleFrames=4)

        SaveAnimation.setKeyFrameManager(keyFrameManager)

    mglw.run_window_config(App)
