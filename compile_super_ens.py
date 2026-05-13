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
F_vals = np.arange(5.0, 15.1, 0.1)

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
                compiled_data[key] = []
                compiled_data[key].append(
                    data[key]
                )
            else:
                compiled_data[key].append(
                    data[key]
                )
        
        # Averaging
        for key, compiled_arr in compiled_data.items():
            compiled_arr = np.array( compiled_arr )
            compiled_arr = np.mean( compiled_arr, axis=0 )

    # ---------------------------------\


    
            
    


compile( 8.0 )