from manim import *

def draw_line_width(w,dir=RIGHT):
    return Line(ORIGIN-dir/2*w , ORIGIN+dir/2*w)

class Jop(Scene):
    def construct(self):
        bitch = Rectangle(width = 4, height = 3, stroke_color = WHITE)
        bitch.set_fill(BLUE, opacity=.5)
        self.play(Write(bitch), run_time=2)

        self.wait(1)
        newtext = Text("Wiggle",font='Calibri', font_size = 77)
        newtext.set_fill(WHITE, opacity=1)
        self.add(newtext)
        self.play(Write(newtext), run_time=1)
        self.wait(1)

        self.play(Unwrite(newtext), run_time=2)
        self.remove(newtext)
        self.wait(1)

        corcle = Circle(radius = 3)
        corcle.set_fill(PINK, opacity=.2)
        self.play(Write(corcle), run_time=.7)

        self.wait(1)

        hlighted = Circle(radius = 3, stroke_color = WHITE)
        hlighted.set_fill(YELLOW, opacity=.7)
        self.play(Write(hlighted))
        self.wait(1)

        leeen = draw_line_width(7,UP)
        leeen.move_to([3.15,0,0])
        self.add(leeen)
        self.wait(1)
        self.play(leeen.animate.move_to([-3.15,0,0]))
        self.wait(.5)
        self.play(leeen.animate.move_to([3.15,0,0]))
        self.wait(.5)
        self.play(leeen.animate.move_to([-3.15,0,0]))
        self.wait(.5)
        self.play(leeen.animate.rotate(PI/2))
        self.wait()
