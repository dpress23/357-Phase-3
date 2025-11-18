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

# set all the values of the edl
edl_system['altitude'] = 11000    # [m] initial altitude
edl_system['velocity'] = -590     # [m/s] initial velocity
edl_system['parachute']['deployed'] = True   # our parachute is open
edl_system['parachute']['ejected'] = False   # and still attached
edl_system['rover']['on_ground'] = False # the rover has not yet landed
tmax = 2000

# create the parachute diameter array
parachute_diam = np.arange(14, 19, 0.5)

# create the empty arrays for time, velocity, and success
tfinal = np.zeros(len(parachute_diam))
vfinal = np.zeros(len(parachute_diam))
sfinal = np.zeros(len(parachute_diam))

for i in range(len(parachute_diam)):
    # run the redifining function and simulate rover
    edl_system = redefine_edl_system(edl_system)
    edl_system['parachute']['diameter'] = parachute_diam[i]
    
    [t,Y, edl_system] = simulate_edl(edl_system, mars, mission_events, tmax, True)
    
    # update final times with the last time value
    tfinal[i] = t[-1]
    
    # update the final velocity by accessing it
    vfinal[i] = edl_system['velocity']
    
    # check the conditions of success and then attribute value
    if(edl_system['velocity'] <= 1.0 and edl_system['altitude'] >= 4.5):
        sfinal[i] = 1.0
    else:
        sfinal[i] = 0.0
    
plt.figure(figsize=(10,10))

plt.subplot(3, 1, 1)
plt.xlabel('Parachute Diameter [m]')
plt.ylabel('Time [s]')
plt.title('EDL Performance vs Parachute Size')
plt.plot(parachute_diam, tfinal, linestyle = '--')

plt.subplot(3, 1, 2)
plt.xlabel('Parachute Diameter [m]')
plt.ylabel('Touchdown Speed [m/s]')
plt.plot(parachute_diam, vfinal, linestyle = '--')

plt.subplot(3, 1, 3)
plt.xlabel('Parachute Diameter [m]')
plt.ylabel('Landing Success [T/F]')
plt.plot(parachute_diam, sfinal, linestyle = '--', marker = '.')

plt.subplots_adjust(hspace=0.5)

    




