"""Assorted stimuli"""

# Copyright (c) 2001-2002 Andrew Straw.  Distributed under the terms of the
# GNU Lesser General Public License (LGPL).

####################################################################
#
#        Import all the necessary packages
#
####################################################################

import types
import VisionEgg.Core
import OpenGL.GL
gl = OpenGL.GL

import string

__version__ = VisionEgg.release_name
__cvs__ = string.split('$Revision$')[1]
__date__ = string.join(string.split('$Date$')[1:3], ' ')
__author__ = 'Andrew Straw <astraw@users.sourceforge.net>'

class Target2D(VisionEgg.Core.Stimulus):
    parameters_and_defaults = {'on':(1,
                                     types.IntType),
                               'color':((1.0,1.0,1.0,1.0),
                                        types.TupleType),
                               'anti_aliasing':(1,
                                                types.IntType),
                               'orientation':(0.0,
                                              types.FloatType),
                               'center':((320.0,240.0),
                                         types.TupleType),
                               'size':((64.0,16.0),
                                       types.TupleType)}
                        
    def __init__(self,projection=None,**kw):
        apply(VisionEgg.Core.Stimulus.__init__,(self,),kw)

    def draw(self):
        if self.parameters.on:
            gl.glMatrixMode(gl.GL_MODELVIEW)
            gl.glLoadIdentity()
            gl.glTranslate(self.parameters.center[0],self.parameters.center[1],0.0)
            gl.glRotate(self.parameters.orientation,0.0,0.0,1.0)

            c = self.parameters.color
            gl.glColor(c[0],c[1],c[2],c[3])
            gl.glDisable(gl.GL_TEXTURE_2D)
            gl.glDisable(gl.GL_BLEND)

            w = self.parameters.size[0]/2.0
            h = self.parameters.size[1]/2.0
            gl.glBegin(gl.GL_QUADS)
            gl.glVertex3f(-w,-h, 0.0);
            gl.glVertex3f( w,-h, 0.0);
            gl.glVertex3f( w, h, 0.0);
            gl.glVertex3f(-w, h, 0.0);
            gl.glEnd() # GL_QUADS

            if self.parameters.anti_aliasing:
                # GL_POLYGON_SMOOTH doesn't seem to work
                # We've already drawn a filled polygon (aliased),
                # now redraw the outline of the polygon (with anti-aliasing)

                # Calculate coverage value for each pixel of outline
                # and store as alpha
                gl.glEnable(gl.GL_LINE_SMOOTH)
                # Now specify how to use the alpha value
                gl.glBlendFunc(gl.GL_SRC_ALPHA,gl.GL_ONE_MINUS_SRC_ALPHA)
                gl.glEnable(gl.GL_BLEND)

                # Draw a second polygon in line mode, so the edges are anti-aliased
                gl.glPolygonMode(gl.GL_FRONT_AND_BACK,gl.GL_LINE)
                gl.glBegin(gl.GL_QUADS)
                gl.glVertex3f(-w,-h, 0.0);
                gl.glVertex3f( w,-h, 0.0);
                gl.glVertex3f( w, h, 0.0);
                gl.glVertex3f(-w, h, 0.0);
                gl.glEnd() # GL_QUADS

                # Set the polygon mode back to fill mode
                gl.glPolygonMode(gl.GL_FRONT_AND_BACK,gl.GL_FILL)