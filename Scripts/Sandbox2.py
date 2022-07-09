from manim import *
from intervals import *
import numpy as np
import warnings

class Curvy(Scene):
    def construct(self):

        def sinusoid(t,n,amplitude):
            a = amplitude
            return np.array([3*t,a*np.sin(n*PI*t),0])

        gamma = [(lambda t : sinusoid(t,n)) for n in range(0,10)]


        a = np.array([-4,3,0])
        b = np.array([-3.5,-3,0])
        c = np.array([4,-2.6,0])
        d = np.array([3,2.7,0])

        max_amp = 0.2
        amp_tracker = ValueTracker(max_amp)
        
        def tri(amp):
            return curved_polygon([a,b,c,d],
                            [lambda t : sinusoid(t,-1,amp),
                             lambda t : sinusoid(t,-2,amp),
                             lambda t : sinusoid(t,-3,amp),
                             lambda t : sinusoid(t,4,amp)],
                            dashed=[1,0,0,1],
                            opaque=[1,1,1,1],
                            npoints = 500,
                            fill_colors=[BLACK,RED,BLACK,RED])

        tri_ref = tri(amp_tracker.get_value())
        if True:
            x,y,z = split(tri_ref,
                          tri_ref["s0"]["p1"].get_center(),
                          tri_ref["s1"]["p2"].get_center())
        if True:
            for sub in tri_ref.submobjects:
                self.play(Create(sub),run_time = 2)

            for sub in tri_ref.submobjects:
                self.remove(sub)
            
        self.add(tri_ref)
        self.wait()

        explode(self,tri_ref,run_time=5)

        self.wait()

        if True:
            tri_ref.add_updater(
                lambda x : x.become(tri(amp_tracker.get_value()))
            )
            
            sign = 1
            for i in range(0,5):
                self.play(amp_tracker.animate.set_value(sign*max_amp),run_time = 2.5)
                sign *= -1

            self.remove(tri_ref)
            self.add(x,y,z)
                   
            self.play(x.animate.shift(RIGHT*2))
            self.play(y.animate.shift(LEFT*2))
        

        
        

        
