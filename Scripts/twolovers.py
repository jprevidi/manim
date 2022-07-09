from manim import *
from intervals import *
from paths import *

class TwoLovers(MovingCameraScene):
    def construct(self):

        def playlong(*args,time = 2):
            self.play(*args, run_time = time)

        def rest(time = 0.2):
            self.wait(time)

        two_lovers = Tex("Two lovers")
        forbidden = Tex("Forbidden from one another")
        war = Tex("War divides their people")
        mountain = Tex("and a mountain divides them apart")
        built = Tex("built a path to be together...")

        mountain_svg = SVGMobject("media\\images\\video_draft\\Mountain_Icon.svg").set_height(3).set_color(GREEN)

        a = VGroup(
                curved_polygon([UL,DL,DR,UR],
                                dashed=[0,0,0,0],
                                fill_colors = [GREEN,GREEN,GREEN,GREEN],
                                circle_color=GREEN,
                                interior_color = RED,
                                opaque = [1,1,1,1]).move_to(LEFT),
                Tex("$\mu$").move_to(LEFT)
            )
        b = VGroup(
                curved_polygon([UL,DL,DR,UR],
                                dashed=[1,1,1,1],
                                fill_colors = [BLACK for i in range(0,4)],
                                circle_color=GREEN,
                                interior_color = RED,
                                opaque = [0,0,0,0]).move_to(RIGHT),
                Tex("$n$").move_to(RIGHT)
            )

        playlong(Write(a),Write(b),Write(two_lovers.move_to(3*UP)), time=2) #two lovers
        playlong(Write(forbidden),a.animate.move_to(LEFT*5),b.animate.move_to(RIGHT*5) , time = 2.44) #forbidden from one another
        rest()
        playlong(forbidden.animate.align_on_at(two_lovers,on=UP,at=DOWN,buffer=DOWN/2),
                 Write(war.align_on_at(forbidden,UP,DOWN,buffer=DOWN/2)), time = 3.18) #war divides their people
        rest(1.18)
        dummy = war.copy().align_on_at(mountain_svg,UP,DOWN,DOWN/2)

        #this is a really cool effect I accidentally made by both writing and aligning at the same time where the
        #words seem to almost drip/rain onto the page
        playlong(Write(mountain), FadeIn(mountain_svg),     #and a mountain divides them apart
                 war.animate.align_on_at(mountain_svg,UP,DOWN,DOWN/2),
                 mountain.animate.align_on_at(dummy,UP,DOWN,DOWN/2),
                 time = 3.52)
        rest(1)
        playlong(Write(built), #built a path to be together
                 time=4.7)
        b.set_z_index(-10)
        b[0]["interior"].set_z_index(-11)
        mountain_svg.set_z_index(-15)
        rest(2.6)

        playlong(a.animate.move_to(LEFT),
                 b.animate.move_to(RIGHT),
                 FadeOut(mountain_svg),FadeOut(two_lovers),
                 FadeOut(forbidden),
                 FadeOut(war),
                 FadeOut(mountain),
                 FadeOut(built),
                 time = 10)

        self.remove(b[0]["s0"]["line"])
        playlong(Unwrite(a[0]["s2"]["line"]))
        self.wait()
        self.wait()
