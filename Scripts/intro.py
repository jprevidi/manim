from manim import *
from intervals import *
from paths import *

def get_boundary(curved_poly):
    grp = VGroup()
    for i in range(len(curved_poly)-1):
        grp += curved_poly["s" + str(i)]
    return grp

class Intro(MovingCameraScene):
    def construct(self):

        def playlong(*args,time = 2):
            self.play(*args, run_time = time)

        def rest(time = 0.2):
            self.wait(time)

        """
        Let's take a buzzfeed quiz: Are you a topologist or a measure theorist?
        (or both?) Pick the bigger square to find out!

        It's likely you're going to think the answer is obvious - if you're a
        topologist, you're going to think one way, and if you're a measure
        theorist you'll think the other way.

        Here is the question: Which of these squares is bigger?
        """

        a = VGroup(
                curved_polygon([UL,DL,DR,UR],
                                dashed=[0,0,0,0],
                                fill_colors = [GREEN,GREEN,GREEN,GREEN],
                                circle_color=GREEN,
                                interior_color = RED,
                                opaque = [1,1,1,1]),
                Tex("$A$").set_opacity(1)
            )
        b = VGroup(
                curved_polygon([UL,DL,DR,UR],
                                dashed=[1,1,1,1],
                                fill_colors = [BLACK for i in range(0,4)],
                                circle_color=GREEN,
                                interior_color = RED,
                                opaque = [0,0,0,0]),
                Tex("$B$").set_opacity(0)
            )

        rest(2)
        playlong(Write(a),time=3.3)
        rest(3)
        """
        Here is the first square, which we're going to call A.
        We're going to then take that exact same square and cut out its center.
        That is, we're going to take these boundary points...
        """
        explode(self, a[0],run_time=4)
        """
        ...and remove them
        """
        rest(2)
        b[0]["s0"].set_opacity(0)
        b[0]["s1"].set_opacity(0)
        b[0]["s2"].set_opacity(0)
        b[0]["s3"].set_opacity(0)
        playlong(a.animate.move_to(2*LEFT),
                 b.animate.move_to(2*RIGHT),
                 time=1.5)
        rest()
        playlong(b[1].animate.move_to(2*RIGHT).set_opacity(1))
        rest(2)

        """
        And we'll call that new square B. To indicate that it's missing its
        boundary points, we're going to use dotted lines and empty circles,
        like so:
        """
        playlong(b[0]["s0"].animate.set_opacity(1),
                 b[0]["s1"].animate.set_opacity(1),
                 b[0]["s2"].animate.set_opacity(1),
                 b[0]["s3"].animate.set_opacity(1))
        rest(2)

        """
        So again, the dotted lines ...
        """
        playlong(Wiggle(get_boundary(b[0])))
        """
        only mean we've taken this infinitely thin
        boundary and removed it.
        """
        self.play(get_boundary(a[0]).animate.shift(2.3*UP))
        rest(3)
        self.play(get_boundary(a[0]).animate.shift(2.3*DOWN))

        """
        A is commonly called a "closed" rectangle while B is called "open"
        """
        openText = Tex("``Open\'\'").next_to(b,direction=DOWN)
        closedText = Tex("``Closed\'\'").next_to(a,direction=DOWN)
        self.play(Write(closedText))
        rest()
        self.play(Write(openText))
        rest(2)

        """
        So, which is larger? A, whose boundary is included, or B, whose boundary
        has been removed?
        """
        self.play(Unwrite(closedText),Unwrite(openText))
        rest()
        which_larger = Tex("Which is larger?",font_size=90).shift(UP*2)
        self.play(Write(which_larger))
        rest()
        rest()
        A_larger = VGroup(
                    Tex("A is larger"),
                    Rectangle(stroke_color = RED,height=1,width=3)
                   ).shift(DOWN*2+LEFT*4)
        self.play(Write(A_larger))
        rest()
        self.play(Wiggle(a))

        rest(1.5)
        B_larger = VGroup(
                    Tex("B is larger"),
                    Rectangle(stroke_color = RED,height=1,width=3)
                   ).shift(DOWN*2+RIGHT*4)
        self.play(Write(B_larger))
        rest()
        self.play(Wiggle(b))
        rest(1.5)
        same_size = VGroup(
                    Tex("They're the same size"),
                    Rectangle(stroke_color = RED,height=1,width=4.8)
                   ).shift(DOWN*2)
        self.play(Write(same_size))
        rest(1)
        self.play(Wiggle(a),Wiggle(b))

        rest(3)


        """
        Part 1: Inside the mind of a topologist
        """
