from App import *

saveAnimation = False

if __name__ == '__main__':
    if saveAnimation:
        App.saveAnimation(name="simple ran 3", fps=60., invisibleFrames=2)

    mglw.run_window_config(App)
