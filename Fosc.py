'''

    This script is the main control interface
    for running a *single* Fosc ens with 
    different settings.


'''

# packages
from run_model import Config, Main
import sys
import numpy as np
import pickle



'''         SETTINGS FOR F OSC           '''

Fosc_cfg = Config(
    num_gridpts = 40,    # number of grids along lat-ring
    ens_size    = 10000, # number of members in ens
    tot_runtime = 5840,  # how long model should run (steps)
    save_dir    = 'analyzed_data/Fosc/',
)

# Parameter
A = 3 # Amplitude
wavelength = (73 / 32)  # How long one oscillation should take in model time tau
                   # For seasonal oscillation, let 1 tau = 5 days =>
                   #               dt = 0.05 = ~6 hours
vshift = 9 # Mean forcing

# Constants
PI = np.pi




# Forcing Functions
def osc_forcing( tau ):
    coef = 2 * PI / wavelength 
    F = A * np.sin( coef * tau ) + vshift
    return F

def seasonal_forcing( tau ):
    coef = 2 * PI / 73 # 365 * (1 tau / 5 days) = 73
    F = A * np.sin( coef * tau ) + vshift

# Save-name
year_frac = np.round( wavelength / 73, decimals=4 )
Fosc_cfg.save_name = f'Fosc_{year_frac}_year'


'''     RUNNING MODEL WITH GIVEN SETTINGS    '''
analyzed_data = Main( Fosc_cfg, osc_forcing )

fname = Fosc_cfg.save_dir + Fosc_cfg.save_name + '.pkl'
pickle.dump( analyzed_data, open( fname, 'wb' ) )