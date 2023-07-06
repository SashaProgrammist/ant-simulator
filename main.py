from App import *

saveAnimation = True

if __name__ == '__main__':
    if saveAnimation:
        App.saveAnimation(countFrame=10, name="Test 1", isSaveSequence=True,
                          fps=1., fpsSim=60, invisibleFrames=10)

    mglw.run_window_config(App)
