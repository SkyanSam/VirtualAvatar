from scipy.interpolate import CubicSpline

print(CubicSpline([0.0,0.33,0.66,1.0],[0.0,-1.0,2.0,1.0])(0.0))