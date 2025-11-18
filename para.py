import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('P3_students')

from define_edl_system import *
from subfunctions_EDL import *
from define_planet import *
from define_mission_events import *
from redefine_edl_system import *

# define the edl, planet, and mission events
edl_system = define_edl_system_1()
mars = define_planet()
mission_events = define_mission_events()

tmax = 2000  # [s] max simulation time

# parachute diameters: 14 to 19 m in 0.5 m steps (inclusive)
parachute_diam = np.arange(14.0, 19.5, 0.5)

# arrays for time, rover touchdown speed, and success flag
tfinal = np.zeros(len(parachute_diam))
vfinal = np.zeros(len(parachute_diam))
sfinal = np.zeros(len(parachute_diam))

for i, D in enumerate(parachute_diam):
    # reset EDL system to the standard initial conditions
    edl_system = redefine_edl_system(edl_system)

    # set parachute diameter for this run
    edl_system['parachute']['diameter'] = D

    # run the simulation (ITER_INFO=False to avoid spam)
    t, Y, edl_system = simulate_edl(edl_system, mars, mission_events, tmax, False)

    # time at termination
    tfinal[i] = t[-1]

    # --- rover speed relative to ground at termination ---
    # Y[0, -1] : EDL (sky crane) velocity
    # Y[5, -1] : rover velocity relative to sky crane
    vel_edl = Y[0, -1]
    vel_rel_rover = Y[5, -1]
    v_rover_ground = vel_edl + vel_rel_rover
    vfinal[i] = v_rover_ground

    # sky crane altitude at termination
    alt_sky = Y[1, -1]

    # mission success criteria:
    # |rover speed| <= 1.0 m/s AND sky crane altitude >= 4.5 m
    if (abs(v_rover_ground) <= 1.0) and (alt_sky >= 4.5):
        sfinal[i] = 1.0
    else:
        sfinal[i] = 0.0

# -------- plotting --------
plt.figure(figsize=(10, 10))

# 1) simulated time vs parachute diameter
plt.subplot(3, 1, 1)
plt.plot(parachute_diam, tfinal, '--o')
plt.ylabel('Simulation Time [s]')
plt.title('EDL Performance vs Parachute Diameter')
plt.grid(True)

# 2) rover speed at landing vs parachute diameter
plt.subplot(3, 1, 2)
plt.plot(parachute_diam, vfinal, '--o')
plt.ylabel('Rover Speed at Landing [m/s]')
plt.grid(True)

# 3) landing success vs parachute diameter
plt.subplot(3, 1, 3)
plt.plot(parachute_diam, sfinal, '--o')
plt.xlabel('Parachute Diameter [m]')
plt.ylabel('Landing Success [1 = success, 0 = failure]')
plt.yticks([0, 1])
plt.grid(True)

plt.subplots_adjust(hspace=0.5)
plt.show()
