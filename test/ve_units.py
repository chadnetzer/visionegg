#!/usr/bin/env python

DEBUG = 0

import unittest
import VisionEgg
import VisionEgg.Core

if DEBUG:
    import VisionEgg.GLTrace
    VisionEgg.gl = VisionEgg.GLTrace
    VisionEgg.Core.gl = VisionEgg.GLTrace

# Use Python's bool constants if available, make aliases if not
try:
    True
except NameError:
    True = 1==1
    False = 1==0

class VETestCase(unittest.TestCase):
    def setUp(self):
        self.screen = VisionEgg.Core.Screen( size          = (320,240),
                                             fullscreen    = False,
                                             preferred_bpp = 32,
                                             maxpriority   = False,
                                             hide_mouse    = False,
                                             frameless     = False)
        self.ortho_viewport = VisionEgg.Core.Viewport( screen = self.screen )
        
    def tearDown(self):
        del self.screen

    def test_core_screen_get_framerate_fast(self):
        fps = self.screen.get_framerate()

    def test_core_screen_get_framerate_slow(self):
        fps = self.screen.get_framerate(average_over_seconds=0.5)

    def test_texture_pil(self):
        if DEBUG:
            print "test_texture_pil",'*'*80
        
        import VisionEgg.Textures
        if DEBUG:
            VisionEgg.Textures.gl = VisionEgg.GLTrace
        import Image
        import ImageDraw
        
        width, height = self.screen.size
        orig = Image.new("RGB",(width,height),(0,0,0))
        orig_draw = ImageDraw.Draw(orig)
        orig_draw.line( (0,0,width,height), fill=(255,255,255) )
        orig_draw.line( (0,height,width,0),  fill=(255,255,255) )
        texture = VisionEgg.Textures.Texture(orig)
        result = texture.get_texels_as_image()
        self.failUnless(result.tostring()==orig.tostring(),'exact texture reproduction with PIL textures failed')

    def test_texture_stimulus_pil(self):
        if DEBUG:
            print "test_texture_stimulus_pil",'*'*80

        import VisionEgg.Textures
        if DEBUG:
            VisionEgg.Textures.gl = VisionEgg.GLTrace
        import Image
        import ImageDraw

        width, height = self.screen.size
        orig = Image.new("RGB",(width,height),(0,0,0))
        orig_draw = ImageDraw.Draw(orig)
        orig_draw.line( (0,0,width,height), fill=(255,255,255) )
        orig_draw.line( (0,height,width,0),  fill=(255,255,255) )
        texture_stimulus = VisionEgg.Textures.TextureStimulus(
            texture = VisionEgg.Textures.Texture(orig),
            position = (0,0),
            anchor = 'lowerleft',
            )

        self.ortho_viewport.parameters.stimuli = [ texture_stimulus ]
        self.ortho_viewport.draw()
        result = self.screen.get_framebuffer_as_image()
        self.failUnless(result.tostring()==orig.tostring(),'exact texture stimulus reproduction with PIL textures failed')

    def test_texture_stimulus_numpy(self):
        if DEBUG:
            print "test_texture_stimulus_numpy",'*'*80
        
        import VisionEgg.Textures
        if DEBUG:
            VisionEgg.Textures.gl = VisionEgg.GLTrace
        import Numeric

        width, height = self.screen.size

        orig = Numeric.zeros((height,width,3),Numeric.UnsignedInt8)
        orig[ 4, 4,:]=255
        orig[ :, 0,:]=255
        orig[ :,-1,:]=255
        orig[ 0, :,:]=255
        orig[-1, :,:]=255
        texture_stimulus = VisionEgg.Textures.TextureStimulus(
            texture = VisionEgg.Textures.Texture(orig),
            position = (0,0),
            anchor = 'lowerleft',
            mipmaps_enabled = False, # not (yet?) supported for Numeric arrays
            )

        self.ortho_viewport.parameters.stimuli = [ texture_stimulus ]
        self.ortho_viewport.draw()
        result = self.screen.get_framebuffer_as_array()
        if DEBUG:
            print orig[:10,:10,0]
            print result[:10,:10,0]
        self.failUnless(Numeric.allclose(orig,result),'exact texture reproduction with Numeric textures failed')

def suite():
    ve_test_suite = unittest.TestSuite()
    ve_test_suite.addTest( VETestCase("test_core_screen_get_framerate_fast") )
    ve_test_suite.addTest( VETestCase("test_core_screen_get_framerate_slow") )
    ve_test_suite.addTest( VETestCase("test_texture_pil") )
    ve_test_suite.addTest( VETestCase("test_texture_stimulus_pil") )
    ve_test_suite.addTest( VETestCase("test_texture_stimulus_numpy") )
    return ve_test_suite

runner = unittest.TextTestRunner()
runner.run(suite())
