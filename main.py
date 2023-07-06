from App import *

saveAnimation = False

if __name__ == '__main__':
    if saveAnimation:
        App.saveAnimation(countFrame=200, name="new color madness 1",
                          fps=24., fpsSim=60, invisibleFrames=1)

    mglw.run_window_config(App)
