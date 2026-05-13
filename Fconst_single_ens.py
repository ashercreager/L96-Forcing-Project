'''

    This script is the main control interface
    for running a *single* Fconst ens with 
    different settings.


'''

# packages
from run_model import Config, Main
import sys



'''         SETTINGS FOR F CONSTANT        '''

Fconst_cfg = Config(
    num_gridpts = 40,    # number of grids along lat-ring
    ens_size    = 24000, # number of members in ens
    tot_runtime = 400,   # how long model should run (steps)
    save_dir    = 'analyzed_data/Fconst/single_ens/',
)

# Forcing function
F = float( sys.argv[1] )
def const_forcing( tau ):
    return F

# Save-name
Fconst_cfg.save_name = f'Fconst_{F}'


'''     RUNNING MODEL WITH GIVEN SETTINGS    '''
Main( Fconst_cfg, const_forcing )