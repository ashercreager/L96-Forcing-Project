'''

    This script is the main control interface
    for running a *single* Fconst ens with 
    different settings.


'''

# packages
from run_model import Config, Main
import pickle
import sys




'''         SETTINGS FOR F CONSTANT        '''

Fconst_cfg = Config(
    num_gridpts = 40,    # number of grids along lat-ring
    ens_size    = 4000, # number of members in ens
    tot_runtime = 5000,   # how long model should run (steps)
    save_dir    = 'analyzed_data/Fconst/single_ens/default_runs/',
    random_seed = 0
)

# Forcing function
F = 5.3 #float( sys.argv[1] )
def const_forcing( tau ):
    return F

# Save-name
Fconst_cfg.save_name = f'Fconst_{F}'


'''     RUNNING MODEL WITH GIVEN SETTINGS    '''
analyzed_data = Main( Fconst_cfg, const_forcing )

fname = Fconst_cfg.save_dir + Fconst_cfg.save_name + '.pkl'
pickle.dump( analyzed_data, open( fname, 'wb' ) )