from App import *

saveAnimation = True

if __name__ == '__main__':
    if saveAnimation:
        App.saveAnimation(100, "simple ran 2", fps=60., invisibleFrames=59)

    mglw.run_window_config(App)
