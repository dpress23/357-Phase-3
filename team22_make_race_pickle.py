import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from define_experiment import experiment1


def alpha_interpolant(alpha_dist, alpha_deg):
    x = np.asarray(alpha_dist, dtype=float).ravel()
    y = np.asarray(alpha_deg, dtype=float).ravel()

    if x.ndim != 1 or y.ndim != 1 or x.size != y.size:
        raise Exception("dist and deg must be equal length and one dimensional")
    if np.any(np.diff(x) <= 0):
        raise Exception("dist cannot decrease")
    if x.size >= 4:
        cubes = CubicSpline(x, y, bc_type="natural")
        return cubes
    else:
        # Linear interpolation fallback
        def linear(xq):
            return np.interp(np.asarray(xq, dtype=float), x, y)
        return linear


experiment, _end_event = experiment1()

x = experiment["alpha_dist"]
y = experiment["alpha_deg"]

func_alpha = alpha_interpolant(x, y)
x_vals = np.linspace(float(x.min()), float(x.max()), 1000)
y_vals = func_alpha(x_vals)


plt.plot(x_vals, y_vals, label="Terrain angle")
plt.plot(x, y, "*", ms=7, label="Data points")
plt.xlabel("Distance [m]")
plt.ylabel("Terrain angle [deg]")
plt.title("Terrain angle vs Distance")
plt.legend()

plt.show()



