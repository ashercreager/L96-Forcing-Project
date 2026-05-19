'''

    This script is the main control interface
    for running a *single* Fosc ens and saving
    raw x3d output.

    x3d has dimensions: 
    [ time_step (units dt), member, gridpt ]

    For animation purposes, only ~100 member
    are probably needed

'''

# packages
from run_model import Config, Main
import numpy as np
import pickle



'''         SETTINGS FOR F OSC           '''

Fosc_cfg = Config(
    num_gridpts = 40,    # number of grids along lat-ring
    ens_size    = 100, # number of members in ens
    tot_runtime = 4200,  # how long model should run (steps)
    save_dir    = 'raw_output/Fosc/',
    save_raw    = True
)

# Parameter
A = 3 # Amplitude
wavelength = (73)  # How long one oscillation should take in model time tau
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



# Save-name
year_frac = np.round( wavelength / 73, decimals=4 )
Fosc_cfg.save_name = f'Fosc_{year_frac}_year'


'''     RUNNING MODEL WITH GIVEN SETTINGS    '''
_, x3d = Main( Fosc_cfg, osc_forcing )

fname = Fosc_cfg.save_dir + Fosc_cfg.save_name + '.pkl'
pickle.dump( x3d, open( fname, 'wb' ) )