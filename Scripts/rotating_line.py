from manim import *

def norm(v):
    return np.sqrt(v.dot(v))

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::
    """
    v1_u = v1/norm(v1)
    v2_u = v2/norm(v2)
    theta = np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
    if(v1[0]*v2[1] - v1[1]*v2[0]) < 0:
        theta = -theta
    return theta

class rotation(Scene):
    
    def construct(self):
        centerPosition = ORIGIN
        radius = Line(centerPosition, RIGHT)

        self.add(radius)
        self.add(radius.copy())

        angleInDegrees = ValueTracker(0)

        radiusRef = radius.copy()

        radius.add_updater(
            lambda z: z.become(radiusRef).rotate(angleInDegrees.get_value()*DEGREES, about_point=centerPosition))
        for i in range(0,360)[0::45]:
            self.play(angleInDegrees.animate.set_value(i),run_time=2)


