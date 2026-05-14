'''

    This script takes all pickle files produced by
    Fconst_super_ens.py for a specific F value and
    averages across each eqbm metric to find the
    super-ens value

'''

# packages
import numpy as np
import pickle
from pathlib import Path

# user-settings
rootpath = Path('analyzed_data/Fconst/single_ens/')
F_vals = np.arange(5.0, 15.1, 0.1).round(2)
savedir = 'analyzed_data/Fconst/super_ens/'

# Compiling function for a single F value 
def compile( F ):

    compiled_data = {}

    for folder in rootpath.glob('seed*'):
        # Grabbing data from each individual run
        # via the naming convention seed0, seed1, ...
        fname = str(folder) + f'/Fconst_{F}.pkl'
        data = pickle.load( open(fname, 'rb') )

        for key in data:

            if key not in compiled_data:
                # Create key if non existent
                compiled_data[key] = []

            compiled_data[key].append( data[key] )
        # -----------------------------------\
    # ---------------------------------\

    # Averaging
    for key, datalist in compiled_data.items():
        # COmputing the super-ens average of each metric
        arr = np.array( datalist )
        compiled_arr = np.mean( arr, axis=0 )
        # Plugging back into compiled_data
        compiled_data[key] = compiled_arr

    # Saving
    savename = savedir + f'super_ens_{F}.pkl'
    pickle.dump( compiled_data, open(savename, 'wb') )


# Looping over several F values
for F in F_vals:
    compile(F)