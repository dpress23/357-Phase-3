"""###########################################################################
#   EDL system dictionary definitions and team race design for project Phase 4.
#
#   NOTE:
#   - define_edl_system_1() below is your old Phase 3 style dictionary.
#   - For Phase 4 Section 1.2, we now start from the provided
#     define_edl_system() function, modify a few fields, add
#     team_number / team_name, and save a .pickle file.
#
#   Created by: Former Marvin Numerical Methods Engineering Team + Group 22
#   Last Modified: (update this date if you want)
###########################################################################"""

import numpy as np
import pickle

from define_rovers import *
from define_edl_system import define_edl_system
from define_chassis import define_chassis
from define_motor import define_motor
from define_batt_pack import define_batt_pack


def define_edl_system_1():
    """
    Legacy Phase 3 EDL system (not used for Phase 4 race).
    Kept here in case you still want to compare with your old design.
    """

    # parachute dict.  Includes physical definition and state information.
    parachute = {
        'deployed': True,   # true means it has been deployed but not ejected
        'ejected': False,   # true means parachute no longer is attached to system
        'diameter': 16.25,  # [m] (MSL is about 16 m)
        'Cd': 0.615,        # [-] (0.615 is nominal for subsonic)
        'mass': 185.0       # [kg] (wild guess -- no data found)
    }

    # Rocket dict.  This defines a SINGLE rocket.
    rocket = {
        'on': False,
        'structure_mass': 8.0,                 # [kg] everything not fuel
        'initial_fuel_mass': 230.0,            # [kg]
        'fuel_mass': 230.0,                    # [kg] current fuel mass (<= initial)
        'effective_exhaust_velocity': 4500.0,  # [m/s]
        'max_thrust': 3100.0,                  # [N]
        'min_thrust': 40.0                     # [N]
    }

    speed_control = {
        'on': False,              # indicates whether control mode is activated
        'Kp': 2000,               # proportional gain term
        'Kd': 20,                 # derivative gain term
        'Ki': 50,                 # integral gain term
        'target_velocity': -3.0   # [m/s] desired descent speed
    }

    position_control = {
        'on': False,             # indicates whether control mode is activated
        'Kp': 2000,              # proportional gain term
        'Kd': 1000,              # derivative gain term
        'Ki': 50,                # integral gain term
        'target_altitude': 7.6   # [m] needs to reflect the sky crane cable length
    }

    # This is the part that lowers the rover onto the surface
    sky_crane = {
        'on': False,            # true means lowering rover mode
        'danger_altitude': 4.5, # [m] altitude at which considered too low
        'danger_speed': -1.0,   # [m/s] speed at which rover would impact too hard
        'mass': 35.0,           # [kg]
        'area': 16.0,           # [m^2] frontal area for drag calculations
        'Cd': 0.9,              # [-] coefficient of drag
        'max_cable': 7.6,       # [m] max length of cable for lowering rover
        'velocity': -0.1        # [m/s] speed at which sky crane lowers rover
    }

    # Heat shield dict
    heat_shield = {
        'ejected': False,  # true means heat shield has been ejected from system
        'mass': 225.0,     # [kg] mass of heat shield
        'diameter': 4.5,   # [m]
        'Cd': 0.35         # [-]
    }

    rover = define_rover_4()

    # Pack everything together.
    edl_system = {
        'altitude': np.NaN,   # system state variable updated throughout simulation
        'velocity': np.NaN,   # system state variable updated throughout simulation
        'num_rockets': 8,     # system level parameter
        'volume': 150,        # system level parameter
        'parachute': parachute,
        'heat_shield': heat_shield,
        'rocket': rocket,
        'speed_control': speed_control,
        'position_control': position_control,
        'sky_crane': sky_crane,
        'rover': rover
    }

    return edl_system


# -------------------------------------------------------------------------
# Phase 4 race design + pickle export
# -------------------------------------------------------------------------

if __name__ == "__main__":

    # 1) Start from the official Phase 4 default system
    edl_system = define_edl_system()

    # 2) Lock in your discrete design choices

    # 2a) Chassis material: 'steel', 'magnesium', or 'carbon'
    edl_system = define_chassis(edl_system, 'carbon')

    # 2b) Motor choice: 'base', 'base_he', 'torque', 'torque_he', 'speed', 'speed_he'
    edl_system = define_motor(edl_system, 'speed_he')   # racing-oriented choice

    # 2c) Battery pack: (battery type, number of modules)
    #    Battery options include 'LiFePO4', 'NiMH', 'NiCD', 'PbAcid-1', 'PbAcid-2', 'PbAcid-3'
    edl_system = define_batt_pack(edl_system, 'LiFePO4', 10)

    # 3) Set your continuous design variables (within your narrowed ranges)

    # 3a) Parachute diameter: target ~16.5 m in [16.0, 17.5]
    #     Try Phase 4 structure first; fall back to old top-level structure if needed.
    try:
        edl_system['edl']['parachute']['diameter'] = 16.5
    except KeyError:
        # Old-style dict (Phase 3 like define_edl_system_1)
        edl_system['parachute']['diameter'] = 16.5

    # 3b) Chassis mass: 250–415 kg, choose 250 kg for light, strong carbon fiber chassis
    edl_system['rover']['chassis']['mass'] = 250.0

    # 4) Add team information at the TOP level of the dict (required for Phase 4 Section 1.2)
    edl_system['team_number'] = 22
    edl_system['team_name'] = "Group 22 Phase 4 Racer"

    # 5) Save to the required .pickle filename
    #    IMPORTANT: replace 'SecYY' with your actual section number (e.g., Sec501).
    filename = "FA25_SecYY_Team22.pickle"  # TODO: change YY to your real section

    with open(filename, "wb") as f:
        pickle.dump(edl_system, f)

    print(f"Saved race design EDL system to {filename}")
