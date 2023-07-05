from App import *

saveAnimation = True

if __name__ == '__main__':
    if saveAnimation:
        App.saveAnimation(5000, "simple ran")

    mglw.run_window_config(App)
