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
    `name = str(countFrame) + '_'`
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
  - if `True` images starting with `name` in the [folder](animation/animationTemp) will be removed
  - if `False` images starting with `name` in the [folder](animation/animationTemp) will be will remain

### result

video save in [animation/saveAnimation](animation/saveAnimation)

---

## video with setting keyframes mode

### how to activate

```python
from App import *
from KeyFrameManager import KeyFrameManager
from DeBug import PosibleToSet

keyFrameManager = KeyFrameManager()

keyFrameManager.addKeyFrame(120, **{
    PosibleToSet.alfa: 0,
    PosibleToSet.texture: 3})
keyFrameManager.addKeyFrame(240, **{
    PosibleToSet.alfa: 1})

App.saveAnimation(countFrame=360, 
                  name="demonstration keyFrameManager",
                  fps=24., fpsSim=60, invisibleFrames=4)

SaveAnimation.setKeyFrameManager(keyFrameManager)

mglw.run_window_config(App)
```

more complex [example](examples/example%20KeyFrameManager.md#example-keyframemanager-)

### options

#### `init KeyFrameManager`

- `interpolationFunction: Callable[[float], float] = lambda x: x * x * (3 - 2 * x))`  
interpolation function for interpolated values between keyframes  
examples:
  - `lambda x: x` - linear
  - `lambda x: x * x * (3 - 2 * x))` - simple smooth
  - `lambda x, k=10: (-exp(k*(x - 1)) - exp(k*(x - 1/2)) + exp(-k/2) + exp(-k))/(-exp(k*(x - 1/2)) + exp(k*(x - 3/2)) - 1 + exp(-k))` -
  smooth (`k` - smoothing factor)  
  here is a [link](https://www.desmos.com/calculator/wxt2aa6nb2?lang=ru) to look at the function in desmos

#### `addKeyFrame`

- `frameIndex: int`  
the index of the frame to which the keyframe is applied
- posible to set:
  - `PosibleToSet.channels : str | ndarray` -
    - if `str` the value will be decoded according to [these](#manage-rgb-channels) rules
    - if `ndarray` array shape must be (3, 3) or (3, )
      - (3, 3) shape - new color = channels.T * color
      - (3, ) shape - the array is converted into a matrix of the form (3, 3) where the values on the main diagonal will be equal to the original ones
  - `PosibleToSet.isRenderAnt : bool` -  
    - if `True` ants will render
    - if `False` ants will not render
  - `PosibleToSet.isRenderPheromoneWar : bool` -  
    - if `True` PheromoneWar will render
    - if `False` PheromoneWar will not render
  - `PosibleToSet.alfa : float | int` -  
    the value of the alpha channel of the texture displayed by the debug
  - `PosibleToSet.texture : int` -  
    index the texture displayed by the debug

### result

video save in [animation/saveAnimation](animation/saveAnimation). it will change the parameters according to the keyframes

---

# runtime simulation control

## deBug modes

### display texture

#### how to activate and deactivate

hold down <kbd>SHIFT</kbd> then
enter the texture index you want to render then
stop pressing <kbd>SHIFT</kbd>

if hold down <kbd>SHIFT</kbd> then stop pressing <kbd>SHIFT</kbd>
display texture deactivate

#### how to manage

manipulation algorithm

hold down <kbd>CTRL</kbd> then
press a special button then
enter kode then
stop pressing <kbd>CTRL</kbd>

press order (press special button and enter kode) is not important  
you can press a special button in the middle of writing code  
only the last pressed a special button is important

##### manage RGB channels

hold down <kbd>CTRL</kbd> then
press <kbd>C</kbd> then
enter RGB kode then
stop pressing <kbd>CTRL</kbd>

press <kbd>SLASH</kbd> perceived as <kbd>SPACE</kbd> 

how is encoded RGB mod:

###### short codes
if the code is less than 3:  
order is not important. if channel in kode, channel will be shown.  
[examples](examples/examples%20RGB%20mode.md#examples-rgb-mode-short-codes)

###### medium codes
if the code is greater and equal than 3 and count point is less than 2:  
order is important. only the last 3 characters are important.  
the first character in important means which channel will be instead of red,  
the second character in important means which channel will be instead of green,  
the third character in important means which channel will be instead of blue.  
if instead of the channel will be <kbd>SPACE</kbd> or <kbd>.</kbd> color value is zero.  
[examples](examples/examples%20RGB%20mode.md#examples-rgb-mode-medium-codes)

###### large codes
all other cases:  
the code is divided into blocks the separator is <kbd>.</kbd>.  
order blocks is important. order in blocks is important. only the last 3 blocks are important.  
the first block is responsible for red, the second block is responsible for green, the third block is responsible for blue.  
blocks are divided into sub blocks consisting of a letter and a number that comes after the letter, 
if there was no number it is perceived as 1
numbers sub blocks which have the same letter. this amount means that the color will depend on so many parts of the letter  
[examples](examples/examples%20RGB%20mode.md#examples-rgb-mode-large-codes)

in shader, it looks like [this](resources/shaders/deBag/deBag_fragment_shader.glsl)

how to type fast large codes if blocks same

hold down <kbd>CTRL</kbd> then 
press <kbd>C</kbd> then
enter kode one block then 
press <kbd>S</kbd>  
Necessarily press <kbd>C</kbd> then press <kbd>S</kbd>

##### manage Alfa channel

hold down <kbd>CTRL</kbd> then
press <kbd>A</kbd> then
enter alfa kode then
stop pressing <kbd>CTRL</kbd>

code should look like this  
{numerator}/{denominator1}/.../{denominatorN}  
numerator - decimal or integer  
denominators - integer  
the numerator will be divided by all the denominators. 
alpha channel will be equal to this value

[examples](examples/examples%20alfa%20mode.md#examples-alfa-mode)

---

### display Ants

#### how to activate and deactivate

press <kbd>A</kbd> to turn on and off

#### how to manage

no

### display pheromoneWar

#### how to activate and deactivate

press <kbd>W</kbd> to turn on and off

#### how to manage

no

