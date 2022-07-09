from manim import *
from intervals import *
from paths import *
import numpy as np
import warnings

class Sandbox(MovingCameraScene):
    def construct(self):

        def gamma(t,n):
            return np.array([3*t,np.sin(n*PI*t),0])

        L = []
        for i in range(3,12): #there are 9
            L.append(interval_from_path(lambda t : gamma(t,i),npoints=1000))

        self.play(Write(L[3]))
        explode(self,L[3],run_time = 3)
        if False:
            VGroup(*L[0:3]).arrange().set_y(2)
            VGroup(*L[3:6]).arrange().set_y(0)
            VGroup(*L[6:9]).arrange().set_y(-2)
            self.clear()
            self.play(Write(L[0]))
            M = L[0].copy()
            for i in range(0,len(L)-1):
                if(i == 0):
                    self.add(M)
                self.play(L[i].animate.become(L[i+1]))
            self.play(self.camera.frame.animate.set(width=5))
            self.clear()
            L[0] = M.move_to(ORIGIN)
            for i in range(1,len(L)):
                L[i].move_to(ORIGIN)
            self.play(Create(L[0]))
            for i in range(0,len(L)-1):
                self.play(L[0].animate.become(L[i+1]))
            
        

        
