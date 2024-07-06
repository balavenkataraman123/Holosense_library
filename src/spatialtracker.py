import math
import numpy as np


def eval_func(a, consts): # Helper functions for generic rangefinder. Explained in a different place. 
    [cos_23, dist_23, cos_13, dist_13, cos_12, dist_12] = consts
    bp = func_b(cos_23, dist_23, a)
    cp = func_b(cos_13, dist_13, a)
    return [(bp**2 + cp**2) - (2*cp*bp*cos_12) - (dist_12)**2, bp, cp]

def func_b(cosine, distance, a):
    return ((2*a*cosine) + abs((2*a*cosine) ** 2 + 4*(distance **2 - a**2))**0.5) / 2

def nr_approx_fast(value, epsilon, steps, consts): # newton raphson algorithm
    [difference, bd, cd] = eval_func(value, consts)
    [difference1, bd, cd] = eval_func(value + epsilon, consts)
    derivative = (difference - difference1) / epsilon # calculates the approximate derivative using 2 points
    nextvalue = value + difference/derivative 
    if steps == 0:
        vals = eval_func(nextvalue, consts)
        vals[0] = nextvalue
        return vals
    else:
        return nr_approx_fast(nextvalue, epsilon, steps-1, consts)

class SpatialTracker:
    previous_position = 12 # The program performs the newton-raphson method from the previous predicted distance.
    # The starting value can be anything, it is just set to 12 since I usually sit 12 inches away from my screen.
    
    # These default values are for an average person and average laptop webcam in case the user doesn't want to manually calibrate.   
    # Measured facial keypoint distances for some of my friends, everyone was within a quarter inch of these value, so measurements should be within 10% without calibration.
    
    eedist = 4 # distance between the corners of the eyes
    endist = 3 # distance between the corners of the eyes and the nose.

    # These values are typical of laptop webcams, but must will cause significant difference when using wide angle / telephoto lenses, etc.
    fov = 78.50    
    aspect = 16/9

    single_output = True # If this is set to False it will provide all three vectors.
    # Otherwise it will provide a "viewpoint" coordinate at the bridge of the nose, which will more commonly be used in AR applications

    def __init__(self, **kwargs):
        
        if "fov" in kwargs: self.fov = kwargs["fov"]
        if "aspectratio" in kwargs: self.aspect = kwargs["aspectratio"]
        if "eyenosedistance" in kwargs: self.eedist = kwargs["eyedistance"]; self.endist = kwargs["eyenosedistance"]
        if "single_output" in kwargs: self.single_output = kwargs["single_output"]

        # tangent of horizontal and vertical FOV for converting image plane coordinates into vectors in irl space.
        self.htan = math.tan(self.fov * math.pi / 360) * self.aspect/((self.aspect ** 2 + 1) ** 0.5) # divided by 360 instead of 180 to  calculate half the angle.
        self.vtan = math.tan(self.fov * math.pi / 360) * 1/((self.aspect ** 2 + 1) ** 0.5)
        
    def calculatePosition(self, mediapipe_coordinates):

        mesh_points=np.array([np.multiply([(0.5 - p.x) * 2, (0.5 - p.y) * 2, 1], [self.htan, self.vtan, 1]).astype(np.float32) for p in mediapipe_coordinates.landmark]) # Convert the coordinates into vectors with unit depth.
        
        # select the 3 facial points
        righteye = mesh_points[33]
        lefteye = mesh_points[263]
        nose = mesh_points[19]
        # calculate the length of the vectors
        rel = np.dot(righteye, righteye) ** 0.5
        lel = np.dot(lefteye, lefteye) ** 0.5
        nl  = np.dot(nose, nose) ** 0.5

        # calculate the cosines of the angles between the eyes and nose
        eec = np.dot(righteye, lefteye) / (rel * lel)
        nre = np.dot(righteye, nose) / (rel * nl)
        nle = np.dot(lefteye, nose) / (lel * nl)
        
        # Calculates the distance given the three cosines and three distances.
        [nd, led, red] = nr_approx_fast(self.previous_position, 0.01, 3, [nle, self.endist, nre, self.endist, eec, self.eedist])
        self.previous_position = nd # updates the previous distance for newton raphson algorithm

        # multiply the vectors (with unit depth) by the depths
        nose_coordinates = nose * nd 
        lefteye_coordinates = lefteye * led
        righteye_coordinates = righteye * red

        if self.single_output:
            return (righteye_coordinates + lefteye_coordinates)/2 # point on the bridge of the nose, beween both eyes
        return (righteye_coordinates, lefteye_coordinates, nose_coordinates)
