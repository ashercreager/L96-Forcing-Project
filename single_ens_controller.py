'''

    This script is the main control interface
    for running a *single* ens with different 
    settings.


'''

# packages
from run_model import Config, Main



'''         SETTINGS FOR F CONSTANT        '''

Fconst_cfg = Config(
    num_gridpts = 40,    # number of grids along lat-ring
    ens_size    = 8000, # number of members in ens
    tot_runtime = 400,   # how long model should run (steps)
    save_dir    = 'raw_output/Fconst_output/',
)

# Forcing function
F = 6.0
def const_forcing( tau ):
    return F

# Save-name
Fconst_cfg.save_name = f'Fconst_{F}'


'''     RUNNING MODEL WITH GIVEN SETTINGS    '''
Main( Fconst_cfg, const_forcing )