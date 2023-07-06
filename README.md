# Ant simulator

simple 
ants 
simulator.

---

# comments about used libraries

- moderngl as mgl - project basis
- moderngl_window as mglw - used to create windows
- cv2 - used to create video and image

---

# Operating modes

## standard mode

### how to activate

```python
from App import App, mglw

mglw.run_window_config(App)
```

### options

no

### result

real time simulation 

---

## video mode

### how to activate

```python 
from App import App, mglw

App.saveAnimation()
mglw.run_window_config(App)
```

### options

- `countFrame:  int | None = None`
  - if `int`: is used for indicate count frame in video
  - if `None`: video is saved while rendering is in progress
- `name:  str | None = None`
  - if `str` is used for video title
  - if `None`:
    - if `countFrame` is `int`  
    `name = str(countFrame)`
    - if `countFrame` is `None`  
    `name = "video" `
- `fps: float = 20.`
this is used for indicate frame rete in video
- `fpsSim: int = 60`
this is used for indicate frame rete in simulation
- `invisibleFrames: int = 2`
this is used for indicate count of update not included in video
- `isSaveSequence: bool = False`
this is used to specify whether to save frames falling into the video  
sequence save in [animation/animationTemp](animation/animationTemp)  
  - if `True` images in the [folder](animation/animationTemp) will be removed
  - if `False` images in the [folder](animation/animationTemp) will be will remain

### result

video save in [animation/saveAnimation](animation/saveAnimation)
