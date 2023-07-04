from App import *

saveAnimation = False

if __name__ == '__main__':
    if saveAnimation:
        App.saveAnimation(100)

    mglw.run_window_config(App)
