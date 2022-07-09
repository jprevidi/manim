from manim import *
from paths import *
import numpy as np
import warnings

class Interval(VDict):
    def __init__(
        self,
        start,
        end,
        start_fill,
        end_fill,
        start_opacity,
        end_opacity,
        dashed,
        one_way = False,
        gamma = None,
        npoints = 100,
        circle_color = RED,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.start = start
        self.end = end
        self.start_fill = start_fill
        self.end_fill = end_fill
        self.start_opacity = start_opacity
        self.end_opacity = end_opacity
        self.dashed = dashed
        self.circle_color = circle_color

        r = 0.07
        linear = False

        if gamma is None:
            gamma1 = lambda t : start*(1-t)+end*t ##straight line from start to end
            linear = True
        else:
            gamma1 = gamma

        self.gamma = gamma1

        diff = [r*unit_vector(derivative(gamma1)(0)),
                -r*unit_vector((derivative(gamma1)(1)))]

        def gamma2(t):
            if norm(gamma1(t) - start)<r:
                return start + diff[0]
            elif norm(gamma1(t) - end)<r:
                return end + diff[1]
            else:
                return gamma1(t)

        #TODO - calculate npoints needed for most applications given total variance of function or some calc-based measure of its wonkiness
        #only use 3 points (keeping one for center) if the line is straight (only works if you give None for gamma)
        if linear:
            self.path_vertices = vertices_from_gamma(gamma2,3) ##THIS IS THE INTERNAL STRUCTURE POINTS, NOT THE DISPLAYED VERTICES
        else:
            self.path_vertices = vertices_from_gamma(gamma2,npoints) ##THIS IS THE INTERNAL STRUCTURE POINTS, NOT THE DISPLAYED VERTICES

        self.c1 = Circle(arc_center = self.start,radius=r,fill_color = start_fill,fill_opacity=start_opacity, stroke_color=circle_color)
        self.c2 = Circle(arc_center = self.end,radius=r,fill_color = end_fill,fill_opacity=end_opacity,stroke_color=circle_color)
        if one_way == True:
            self.c2.set_opacity(0)
        path = jagged_path(gamma2,npoints=npoints)
        if dashed == 1:
            self.line = dash(path)
        else:
            self.line = path
        self.add([("line",self.line),("p1",self.c1),("p2",self.c2)])


#TODO - make this expand curved intervals in the direction their ends point
class ExpandInterval(Animation):
    def __init__(self, interval,
                 interpolation_fn = rate_functions.there_and_back,
                 shape_center = None, prior_point = None,
                 next_point = None, radius = 0.5 ,**kwargs):
        super().__init__(interval,**kwargs)
        self.interval = interval
        self.initialp1 = self.interval["p1"].get_center()
        self.initialp2 = self.interval["p2"].get_center()
        self.line_center = self.interval["line"].get_center()
        self.radius = radius
        self.interpolation_fn = interpolation_fn
        if shape_center is None: ##this is to be used if there is no larger shape for the interval to be a part of
            shape_center = self.line_center
        if prior_point is None:
            prior_point = self.initialp2
        if next_point is None:
            next_point = self.initialp1

        self.center = [None,None,None]
        self.center[0] = self.initialp1 - outward_bisector(prior_point, self.initialp1, self.initialp2)
        self.center[1] = self.initialp2 - outward_bisector(self.initialp1, self.initialp2, next_point)
        if norm(shape_center - self.line_center) < 0.02:
            self.center[2] = self.line_center
        else:
            self.center[2] = self.line_center - outward_perp(self.initialp1, self.initialp2, shape_center)

        diff = [self.initialp1 - self.center[0], self.initialp2 - self.center[1], self.line_center - self.center[2]]
        norms = [np.sqrt(diff[0].dot(diff[0])), np.sqrt(diff[1].dot(diff[1])), np.sqrt(diff[2].dot(diff[2]))]
        self.unit = [0,0,0]
        if norms[0] > 0.01:
            self.unit[0] = diff[0]/norms[0]
        if norms[1] > 0.01:
            self.unit[1] = diff[1]/norms[1]
        if norms[2] > 0.01:
            self.unit[2] = diff[2]/norms[2]
    def interpolate_mobject(self,alpha):
        alpha = self.interpolation_fn(alpha)
        unit = self.unit
        r = self.radius
        self.interval["p1"].move_to(self.initialp1 + r*alpha*unit[0])
        self.interval["p2"].move_to(self.initialp2 + r*alpha*unit[1])
        self.interval["line"].move_to(self.line_center + r*alpha*unit[2])

def interval_from_path(gamma,npoints=100,start_fill=BLACK,end_fill=RED,start_opacity=0,end_opacity=1,circle_color=RED,dashed = 0):
        return  Interval(start=gamma(0),
                         end=gamma(1),
                         start_fill = start_fill,
                         end_fill = RED,
                         start_opacity=start_opacity,
                         end_opacity=0,
                         dashed=dashed,
                         one_way=False,
                         gamma = gamma,
                         circle_color = circle_color,
                         npoints = npoints)

def set_gamma(self,gamma):
    self.gamma = gamma
    self.start = gamma(0)
    self.end = gamma(1)

def set_endpoints(interval,start,end):
    interval.set_gamma(set_path_endpoints(gamma,start,end))


def curved_polygon(vertices,gammas=None,opaque=None,fill_colors=None,dashed=None,npoints = 100,circle_color = RED,interior_color = BLUE,**kwargs): #TODO - set defaults for args
        n = len(vertices)
        if gammas is None:
            gammas = [None for i in range(n)]
        #replace any incorrectly formatted gammas with straight lines
        for i, g in enumerate(gammas):
            if g is not None: #and isinstance(g(0), type(np.array([0,0,0]))): #type checking
                pass
            else:
                gammas[i] = lambda t : vertices[i]*(1-t)+vertices[(i+1)%n]*t ##straight line from start to end

        sides = [Interval(start=vertices[i],
                          end=vertices[(i+1)%n],
                          end_fill = BLACK, #red is a placeholder since it's transparent
                          start_opacity=opaque[i],
                          start_fill = fill_colors[i],
                          end_opacity=0,
                          dashed=dashed[i],
                          one_way=True,
                          npoints = npoints,
                          circle_color = circle_color,
                          gamma = set_path_endpoints(gammas[i],vertices[i],vertices[(i+1)%n]), #TODO - set this so it can be a function from R -> R instead of R -> R^2 x {0}
                          ) for i in range(n)]
        points = []
        for side in sides:
            points = points + [side.start] + side.path_vertices
        vd = VDict(show_keys=False)
        for i, side in enumerate(sides):
            vd["s" + str(i)] = side
            layer = side.z_index
        vd["interior"] = VGroup()
        vd["interior"] += Polygon(*points,stroke_opacity=0,fill_opacity=0.4,fill_color=interior_color) #use the key "interior" to access the interior
        for p in vertices:
            ##this is where we cut out unneeded parts of the interior that are inside visible vertices
            #probably should ammend so that it just cuts arcs off instead of adding a black dot
            d = Dot(point = p,color=BLACK,stroke_color = BLACK, fill_opacity=1,radius=0.05)
            vd["interior"] += d
        #send those dots to the background
        for i in range(len((vd["interior"]))):
            vd["interior"][i].z_index = sides[0].z_index - 10
        vd["interior"].z_index = sides[0].z_index - 10
        return vd






#kwargs is opaque/dashed=[array of 0's and 1's] - list 0 for undashed/transparent and 1 for dashed/opaque
#this defines a polygon in the way I want it to be defined so it can be exploded
#it is a VDict(*list of sides (intervals), interior (includes a polygon and bounding dots))
def poly(*points,**kwargs):
        n = len(points)
        sides = [Interval(start=points[i],end=points[(i+1)%n],
                          start_opacity=kwargs.get("opaque")[i], start_fill = kwargs.get("fill_colors")[i],
                          end_opacity=0, end_fill = BLACK, one_way=True, stroke_color = kwargs.get("stroke_color"),#red is a placeholder since it's transparent
                          dashed=kwargs.get("dashed")[i]) for i in range(n)]
        vd = VDict(show_keys=False)
        for i, side in enumerate(sides):
            vd["s" + str(i)] = side
            layer = side.z_index
        vd["interior"] = VGroup()
        vd["interior"] += Polygon(*points,stroke_opacity=0,fill_opacity=0.4,fill_color=BLUE) #use the key "interior" to access the interior
        for p in points:
            d = Dot(point = p,color=BLACK,stroke_color = BLACK, fill_opacity=1,radius=0.05)
            vd["interior"] += d
        for i in range(len((vd["interior"]))):
            vd["interior"][i].z_index = sides[0].z_index - 10
        vd["interior"].z_index = sides[0].z_index - 10
        return vd

def rect(blcorner,length,width,**kwargs):
    return poly(blcorner,
                blcorner+length*np.array([1,0,0]),
                blcorner+length*np.array([1,0,0])+width*np.array([0,1,0]),
                blcorner+width*np.array([0,1,0]),
                **kwargs)
#running with multiple polys is buggy, but it works fine with one
def explode(self, *polys, radius = 0.5, run_time = 1):
    animations = []
    for poly in polys:
        try: #if there's a whole polygon
            vertices = [d.get_center() for d in poly["interior"][1:]]
            n = len(poly) - 1
            intervals = poly.submobjects[0:n]
        except: #if it's just one interval
            vertices = [poly["p1"].get_center(),poly["p2"].get_center()]
            n = 2
            intervals = [poly]
        points = [None for i in intervals]
        for i, interval in enumerate(intervals):
            points[i] = ExpandInterval(interval,shape_center=poly.get_center(),
                                       prior_point = vertices[i-1],
                                       next_point = vertices[(i+2)%n],
                                       radius = radius)
        animations = animations + points
    self.play(*animations,run_time=run_time)

#here assuming v1 and v2 are vertices of poly and the interval between them cuts the polygon into two polygons
def split(polyg, v1, v2, npoints = 100): #cut the polygon (interval format) into three pieces (one interval and two polygons)
    results = [None,None,None]
    vertices = [[],[],[]] #list to hold vertices of the resulting polygons/intervals (first two polys, third is for interval)
    k = 0
    #populate vertex lists
    for i, vertex in enumerate([d.get_center() for d in polyg["interior"][1:]]):
        s = find_side(polyg,vertex)
        print(s.gamma)
        vertices[k].append([s["p1"].get_center(),
                            s["p1"].fill_opacity,
                            s["p1"].get_color(),
                            s.gamma,
                            is_dashed_int(s["line"])])
        if (norm(vertex - v1) < 0.02):
            vertices[k][-1][4] = 1
            vertices[k][-1][3] = lambda t : v1*(1-t)+v2*t ##straight line from start to end
            vertices[k][-1][2] = BLACK
            vertices[2].append([s["p1"].get_center(),
                                s["p1"].fill_opacity,
                                s["p1"].get_color(),
                                s.gamma,
                                1])
            k = (k+1)%2
            #also add to the other vertex list, since it's shared
            vertices[k].append([s["p1"].get_center(),
                                s["p1"].fill_opacity,
                                BLACK,
                                s.gamma,
                                is_dashed_int(s["line"])])
        elif (norm(vertex - v2) < 0.02):
            vertices[k][-1][4] = 1
            vertices[k][-1][3] = lambda t : v1*(1-t)+v2*t ##straight line from start to end
            vertices[k][-1][2] = BLACK
            vertices[2].append([s["p1"].get_center(),
                                s["p1"].fill_opacity,
                                s["p1"].get_color(),
                                s.gamma,
                                1])
            k = (k+1)%2
            #also add to the other vertex list, since it's shared
            vertices[k].append([s["p1"].get_center(),
                                s["p1"].fill_opacity,
                                BLACK,
                                s.gamma,
                                is_dashed_int(s["line"])])
    print('hi', len(vertices[0]) )
    dashed_vals = [None,None,None]
    dashed_vals[0] = extract(4,vertices[0])
    dashed_vals[1] = extract(4,vertices[1])
    dashed_vals[2] = extract(4,vertices[2])

    gammas = [None,None,None]
    gammas[0] = extract(3,vertices[0])
    gammas[1] = extract(3,vertices[1])
    gammas[2] = extract(3,vertices[2])

    fill_colors = [None,None,None]
    fill_colors[0] = extract(2,vertices[0])
    fill_colors[1] = extract(2,vertices[1])
    fill_colors[2] = extract(2,vertices[2])

    opacities = [None,None,None]
    opacities[0] = extract(1,vertices[0])
    opacities[1] = extract(1,vertices[1])
    opacities[2] = extract(1,vertices[2])

    vertices[0] = extract(0,vertices[0])
    vertices[1] = extract(0,vertices[1])
    vertices[2] = extract(0,vertices[2])

    results[0] = curved_polygon(vertices[0],gammas=gammas[0],opaque= [1,1,1,1,1,1,1],fill_colors= fill_colors[0],dashed=dashed_vals[0],npoints = npoints)#TODO --> FIX THIS TO GET ACTUAL OPACITY
    results[1] = curved_polygon(vertices[1],gammas=gammas[1],opaque= [1,1,1,1,1,1,1],fill_colors= fill_colors[1],dashed=dashed_vals[1],npoints = npoints)
    results[2] = Interval(*vertices[2],
                          dashed = 0,
                          start_fill = fill_colors[2][0],
                          end_fill = fill_colors[2][1],
                          start_opacity = 1,
                          gamma = lambda t : v1*(1-t)+v2*t, ##straight line from start to end,
                          end_opacity = 1)
    return results

def extract(nth, ls):
    xs = []
    for elem in ls:
        xs.append(elem[nth])
    return xs


#check if a line is dashed
def is_dashed_int(line):
    if isinstance(line,DashedVMobject):
        return 1
    else:
        return 0

#returns the side on which vertex is p1
def find_side(poly,vertex):
    n = len(poly) - 1
    for interval in poly.submobjects[0:n]:
        if norm(interval["p1"].get_center() - vertex) < 0.02:
            return interval
    raise Exception("Vertex not found")

def dash(obj):
    return DashedVMobject(obj)

def unit_vector(v):
    return v/norm(v)

def norm(v):
    return np.sqrt(v.dot(v))

def outward_perp(p1,p2,center):
    v = np.array([p1[1]-p2[1],p2[0]-p1[0],0])
    a = v/norm(v)
    p = a + (p1 + p2)/2
    b = -v/norm(v)
    q = b + (p1 + p2)/2
    if norm(p - center) < norm(q - center):
        return b
    else:
        return a

def outward_bisector(u,v,w):
    return unit_vector(unit_vector(v-w)+unit_vector(v-u))

def mod(n,k):
    if 0<=n and n<k:
        return n
    elif n < 0:
        return mod(n+k,k)
    else:
        return mod(n-k,k)
