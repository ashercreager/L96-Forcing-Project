'''

    This script plots/compares Fosc
    to what the Fconst eqbm values
    would be at each point for that
    given forcing

    STEP 1: Load all eqbm values into an
    array such that the index of an element
    in this array corresponds to the correct
    index of an 'F value' array'
    

'''

# packages
import numpy as np
import pickle
from pathlib import Path

# ============ LOADING DATA ================

# Keys to extract from each pickle file
eqbm_keys = {
    'mean' : 'eqbm_mean',
    'std' : 'eqbm_std_dev',
    'skew' : 'eqbm_skew',
    'kurt' : 'eqbm_kurt'
}

# Initializing a dictionary to store Fconst eqbm values
# and a list to store their corresponding F values at 
# every index
eqbm_vals = { k : [] for k in eqbm_keys }
F_vals = []

# Looping over all pickle files and storing the 
# the wanted data into eqbm_vals and F_vals
fdir = '../analyzed_data/Fconst/single_ens/'
path = Path(fdir)

for file in path.glob('*.pkl'):
    # Loading pickle file
    fname = fdir + file.name
    data = pickle.load( open(fname, 'rb') )

    # Storing eqbm values
    for store_key, load_key in eqbm_keys.items():
        eqbm_vals[store_key].append( data[load_key] )

    F_vals.append( data['F'] ) 
# ------------- End Loop -------------- \

# Loading Fosc metric data (hardcoded for now)
fdir = '../analyzed_data/Fosc/' 
fname = fdir + 'Fosc_1.0_year.pkl'
Fosc = pickle.load( open(fname, 'rb') )

#  ============ PLOTTING ================
