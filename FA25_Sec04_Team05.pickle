import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from define_experiment import experiment1


def alpha_interpolant(alpha_dist, alpha_deg):
    """
    An interpolating function for the terrain angle.

    Returns the interpolated angle at query distances. 
    It uses a natural cubic spline if there are at least 4 data points, otherwise it falls back to linear interpolation.
    """

    # Convert inputs to 1D float numpy arrays
    x = np.asarray(alpha_dist, dtype=float).ravel()
    y = np.asarray(alpha_deg, dtype=float).ravel()


    # checks shapes and sizes
    if x.ndim != 1 or y.ndim != 1 or x.size != y.size:
        raise Exception("dist and deg must be equal length and one dimensional")

    # the distances must strictly be increasing
    if np.any(np.diff(x) <= 0):
        raise Exception("dist cannot decrease")

    # cubic spline 
    if x.size >= 4:
        cubes = CubicSpline(x, y, bc_type="natural")
        return cubes
    else:
    # Linear interpolation fallback
        def linear(xq):
            return np.interp(np.asarray(xq, dtype=float), x, y)
        return linear


experiment, _end_event = experiment1()


# terrain data
x = experiment["alpha_dist"]
y = experiment["alpha_deg"]


# builds the interpolating function
func_alpha = alpha_interpolant(x, y)

# creates grid of distances
x_vals = np.linspace(float(x.min()), float(x.max()), 1000)

# evaluates the interpolant on this grid
y_vals = func_alpha(x_vals)

# plots the terrain angle function and original data poinrs
plt.plot(x_vals, y_vals, label="Terrain angle")
plt.plot(x, y, "*", ms=7, label="Data points")
plt.xlabel("Distance [m]")
plt.ylabel("Terrain angle [deg]")
plt.title("Terrain angle vs Distance")
plt.legend()

plt.show()



