#!/usr/bin/env python

# Display a moving sinusoidal grating

from VisionEgg.Core import *
from VisionEgg.Gratings import *
from Numeric import *
import pygame

if not hasattr(pygame.display,"set_gamma_ramp"):
    raise RuntimeError("Need pygame 1.5 or greater for set_gamma_ramp function.")

def gamma_func(f):
    r = arange(256).astype('i')
    g = r
    b = zeros((256,),'i')
    if pygame.display.set_gamma_ramp(r,g,b):
        print "Gamma set"
    else:
        print "Gamma failed."

# Initialize OpenGL graphics screen.
screen = get_default_screen()

# Calculate where the lower left corner of the grating must be to be centered
grating_size = 256
grating_left   = (screen.size[0]/2) - (grating_size/2)
grating_bottom = (screen.size[1]/2) - (grating_size/2)

# Create the instance SinGrating with appropriate parameters
stimulus = SinGrating2D(center      = ( grating_left , grating_bottom ),
                        size        = ( grating_size , grating_size ),
                        spatial_freq  = 10.0 / grating_size, # 10 cycles
                        orientation = 90.0 )

# Use viewport with pixel coordinate system for projection
viewport = Viewport(screen=screen,stimuli=[stimulus])

# Create an instance of the Presentation class
p = Presentation(go_duration=(5.0,'seconds'),viewports=[viewport])

# Register the controller functions
p.add_controller(None,None,FunctionController(during_go_func=gamma_func,temporal_variables=Controller.FRAMES_SINCE_GO))

# Go!
p.go()
