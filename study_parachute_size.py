import numpy as np
import matplotlib.pyplot as plt
import sys
'''
MEEN 357 Group 22 Phase 3 study_parachute_size 

We are trying to model the termination time, rover speed
at termination, and whether or not the mission was successful
at a variety of parachute diameters (14m - 19m: step size = 0.5 m)
'''
# Import Mission Parameters
from define_edl_system import *
from subfunctions_EDL import *
from define_planet import *
from define_mission_events import *
from redefine_edl_system import *

# Define the system parameters for the EDL,events, and planet.
edl_system = define_edl_system_1()
events = define_mission_events()
mars = define_planet()

# EDL Values
edl_system['altitude'] = 11000  # (m) Default Initial Altitude
edl_system['velocity'] = -590  # (m/s) Default Initial Velocity
edl_system['parachute']['deployed'] = True  # We want an Open Parachute
edl_system['parachute']['ejected'] = False  # Parachute is open but not detached yet
edl_system['rover']['on_ground'] = False  # Rover is not
tmax = 2000

# Tests all parachutes with diameters between (14m and 19m; step size 0.5m)
diameter_parachute = np.arange(14, 19, 0.5)

# Final Parameters List, Created and set to zero before the for loop
time_f = np.zeros(len(diameter_parachute))
velocity_f = np.zeros(len(diameter_parachute))
success_f = np.zeros(len(diameter_parachute)) # Final parameter for sucess

#Loop that checks if edl system
for i in range(len(diameter_parachute)): # runs through all different parachutes
    # Re-builds the system based off the specific parachute diameter being tested
    edl_system = redefine_edl_system(edl_system)
    edl_system['parachute']['diameter'] = diameter_parachute[i]
    [t, Y, edl_system] = simulate_edl(edl_system, mars, events, tmax, True)
    time_f[i] = t[-1] # Final Time after run
    velocity_f[i] = edl_system['velocity'] # Final Velocity after run

# Success Check
    if (edl_system['velocity'] <= 1.0 and edl_system['altitude'] >= 4.5): # Velocity must be <= 1 m/s and altitude must be >= 4.5 m
        success_f[i] = 1.0 # run is successful :) !!!
    else:
        success_f[i]= 0.0 # run isn't successful :(

# Formatting
plt.figure(figsize=(10, 10))
plt.suptitle('EDL Run Performance Over Varying Parachute Sizes',fontsize=16, fontweight='bold')

# Parachute Diameter vs Time
plt.subplot(3, 1, 1)
plt.xlabel('Diameter (m)')
plt.ylabel('Time (s)')
plt.title('Parachute Diameter vs Time')
plt.plot(diameter_parachute, time_f, linestyle='--', marker='.',)

# Parachute Diameter vs Touchdown Speed'
plt.subplot(3, 1, 2)
plt.xlabel('Diameter (m)')
plt.ylabel('Speed (m/s)')
plt.title('Parachute Diameter vs Touchdown Speed')
plt.plot(diameter_parachute, velocity_f, linestyle='--', marker='.',)

# Parachute Diameter vs Landing Success
plt.subplot(3, 1, 3)
plt.xlabel('Diameter (m)')
plt.ylabel('Success (T/F])')
plt.title('Parachute Diameter vs Landing Success')
plt.plot(diameter_parachute, success_f, linestyle='--', marker='.',)

plt.subplots_adjust(hspace=0.5) ##  Corresponds with step size

plt.show()


    





