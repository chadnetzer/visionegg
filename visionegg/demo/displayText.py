#!/usr/bin/env python
"""Display text strings."""

from VisionEgg.Core import *
from VisionEgg.Text import *
import math

screen = get_default_screen()
screen.parameters.bgcolor = (0.0,0.0,1.0,1.0) # background white (RGBA)

text = Text(text="Hello world!",
            color=(1.0,1.0,1.0,0.0), # alpha is ignored (set with max_alpha_param)
            position=(screen.size[0]/2,screen.size[1]/2),
            font_size=50,
            anchor='center')

viewport = Viewport(screen=screen,
                    size=screen.size,
                    stimuli=[text])
p = Presentation(go_duration=(5.0,'seconds'),viewports=[viewport])
p.go()
