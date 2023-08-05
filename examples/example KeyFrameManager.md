# example KeyFrameManager 

```python
from App import *
from KeyFrameManager import KeyFrameManager
from DeBug import PosibleToSet


if __name__ == '__main__':
    keyFrameManager = KeyFrameManager()

    keyFrameManager.addKeyFrame(0, **{
        PosibleToSet.texture: 3})
    keyFrameManager.addKeyFrame(12, **{
        PosibleToSet.alfa: 0})
    keyFrameManager.addKeyFrame(24, **{
        PosibleToSet.alfa: 1,
        PosibleToSet.isRenderAnt: True})
    keyFrameManager.addKeyFrame(36, **{
        PosibleToSet.isRenderAnt: False,
        PosibleToSet.channels: "rgb"})
    keyFrameManager.addKeyFrame(48, **{
        PosibleToSet.channels: "r"})
    keyFrameManager.addKeyFrame(60, **{
        PosibleToSet.channels: "rgb"})
    keyFrameManager.addKeyFrame(72, **{
        PosibleToSet.channels: "g"})
    keyFrameManager.addKeyFrame(84, **{
        PosibleToSet.channels: "rgb"})
    keyFrameManager.addKeyFrame(96, **{
        PosibleToSet.channels: "b"})
    keyFrameManager.addKeyFrame(108, **{
        PosibleToSet.channels: "rgb"})

    App.saveAnimation(countFrame=120, name="Test",
                      fps=24., fpsSim=60, invisibleFrames=4)

    SaveAnimation.setKeyFrameManager(keyFrameManager)

    mglw.run_window_config(App)

```