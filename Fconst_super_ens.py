'''

    This script is the main control interface
    for running a multiple Fconst ensembles
    with different random_seeds for the purpose
    of building a 'super-ensemble'.

    From previous model runs, the behavior of the
    initial equilibration phase was much more
    dependent on random-seed than ens-size:
    increasing ens-size to significantly larger
    values like 100,000 did little to change
    'noise' behavior during this early window,
    whereas random-seed changed it a lot.

    Building a super-ens might help build a 
    'truer' picture of general distribution behavior?? 

'''

# packages
from run_model import Config, Main
import pickle
import numpy as np
import os
import sys

# user-settings
cfg = Config(
    num_gridpts = 40,    # number of grids along lat-ring
    ens_size    = 5000, # number of members in ens
    tot_runtime = 500,   # how long model should run (steps)
    save_dir    = 'analyzed_data/Fconst/single_ens/'
)
seeds = np.arange(0,41)

# Defining forcing function F
F = float( sys.argv[1] )
def const_forcing( tau ):
    return F

# RUN LOOP
for seed in seeds:

    # Running model
    cfg.random_seed = seed
    output = Main( cfg, const_forcing )

    save_folder = cfg.save_dir + f'seed{seed}/'
    # Make save directory if it doesn't yet exist
    os.makedirs(save_folder, exist_ok=True)

    # Dumping data
    savename = save_folder + f'Fconst_{F}.pkl'
    pickle.dump( output, open(savename, 'wb') )

    # Done!
    print(f'seed {seed} dumped')
    