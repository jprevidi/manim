from manim import *
from intervals import *
import numpy as np
import warnings

class MovingDots(Scene):
    def construct(self):

        text = Text("Hello, Claire!\nLook what I made!", font_size=60).shift(DOWN*2.5)
        bl = np.array([-1,-1,0])
        tl = np.array([-1,2,0])
        polygon = poly(np.array([-2,0,0]),bl,tl,dashed=[1,0,0],opaque=[1,1,0],fill_colors=[BLACK,RED,BLACK])
        rectangle = rect(np.array([-1,-1,0]),2,3,dashed=[0,0,0,1],opaque=[0,1,0,0],fill_colors = [BLACK,RED,BLACK,BLACK])
        tri = poly(np.array([2,0,0]),np.array([1,-1,0]),np.array([1,2,0]),dashed=[1,0,1],opaque=[0,1,1],fill_colors=[BLACK,RED,RED])
        s = Interval(np.array([1,-1,0]),np.array([1,2,0]), dashed = 0, start_fill = RED, end_fill = RED, start_opacity = 1, end_opacity = 0)
        hverts = RegularPolygon(6).get_vertices()
        hexagon = poly(*hverts,dashed = [0,1,1,0,1,0], opaque = [1 for i in range(6)], fill_colors = [BLACK,RED,RED,BLACK,BLACK,RED])

        VGroup(hexagon, tri,rectangle).set_x(0).arrange(buff=1.8)
        
        self.play(Write(tri),Write(hexagon),Write(rectangle),run_time=3)
        self.wait()
        explode(self,tri,run_time = 3)
        explode(self,hexagon,run_time = 3,radius = 0.5)
        explode(self,rectangle,run_time = 3)
        self.play(Rotate(hexagon,angle=2*PI,rate_func = smooth))
        self.play(Rotate(tri,angle=2*PI,rate_func = smooth))
        self.play(Rotate(rectangle,angle=2*PI,rate_func = smooth))
        self.play(FadeIn(s))
        self.play(Rotate(s,angle=PI/2,about_point=tl+np.array([2,0,0])))
        self.play(s.animate.shift(UP))
        explode(self,s)

        self.clear()
        print(rectangle["s1"]["p1"].get_center())
        print(rectangle["s2"]["p2"].get_center())
        split_hex = split(hexagon,
                           hexagon["s1"]["p1"].get_center(),
                           hexagon["s4"]["p2"].get_center())
        a, b, c = split_hex
        #VGroup(a,b,c).set_x(0).arrange(buff=1.8)
        a["s1"]["line"].set_opacity(0)
        b["s4"]["line"].set_opacity(0)
        self.play(Write(a),Write(b),Write(c["p1"]), Write(c["p2"]), run_time=3)
        self.wait(2)
        self.play(Write(c["line"]),run_time=1.5)
        a["s1"]["line"].set_opacity(1)
        b["s4"]["line"].set_opacity(1)
        self.wait(3)
        self.play(a.animate.move_to([-3,0,0]),b.animate.move_to([0,0,0]),c.animate.move_to([3,0,0]))
        self.wait(3)
        self.play(a.animate.move_to([1,0,0]),b.animate.move_to([0,0,0]))
        self.play(c.animate.move_to([b["s0"]["p1"].get_center()[0],0,0]))
        self.wait(2)
        self.play(Uncreate(c["line"]),Unwrite(a["s1"]["line"]),Uncreate(b["s4"]["line"]))
        self.wait()
        self.clear()
        x = VGroup(a,b,c)
        self.add(hexagon.move_to(x.get_center()))
        explode(self,hexagon)
        self.wait()


        
