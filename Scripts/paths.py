from manim import *
from intervals import *
import numpy as np
import warnings

#move this to utility module
def getmiddle(ls):
    index = (len(ls)-1)//2
    return ls[index]

class Path(Line):
    def __init__(
        self,
        gamma,
        npoints,
        buff=0,
        path_arc = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.start = gamma(0)
        self.end = gamma(1)
        self.gamma = gamma
        self.npoints = npoints
        self.buff = buff
        self.path_arc = path_arc
        
    def get_path_length(self, nintervals = None):
        if nintervals is None:
            nintervals = self.npoints-1
        return path_length(self.gamma,nintervals)

def vertices_from_gamma(gamma,npoints : int,lower_bound = 0, upper_bound = 1):
    interval_length = upper_bound - lower_bound
    return [gamma(t/(npoints-1)*interval_length + lower_bound) for t in range(0,npoints)]

def jagged_path(gamma, npoints=100, lower_bound = 0., upper_bound = 1.):
    L = Path(gamma,npoints)
    points = vertices_from_gamma(gamma,npoints,lower_bound,upper_bound)
    L.set_points_as_corners(points)
    return L

def smooth_path(gamma):
    return jagged_path(gamma).make_smooth()

def path_length(gamma, nintervals=100):
    return sum([ norm( gamma((t+1)/nintervals) - gamma(t/nintervals) ) for t in range(0,nintervals)])

def linear_path(start,end):
    def gamma(t):
        if t==0:
            return start
        else:
            return end
    return jagged_path(gamma,2)

def derivative(gamma):
    h = 0.001
    return lambda x : (gamma(x+h)-gamma(x))/h

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

def rotate(f,theta):
    cos = np.cos(theta)
    sin = np.sin(theta)
    #rotation matrix
    rot = np.array([[cos,-sin,0],
                    [sin,cos,0],
                    [0,0,0]])
    return lambda t : np.dot(rot,f(t))

def scale(f,beta):
    return lambda t : f(t)*beta

def translate(f,v):
    return lambda t : f(t) + v

#this will scale, translate, and rotate gamma so that its endpoints are start and end
def set_path_endpoints(gamma,start,end): #DOES NOT MODIFY GAMMA
    f = gamma
    theta = angle_between(gamma(1)-gamma(0), end - start)
    f = rotate(f, theta)
    scale_factor = norm(end - start)/norm(gamma(1)-gamma(0))
    f = scale(f, scale_factor)
    f = translate(f,start - f(0))

    return f
    

