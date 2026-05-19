'''

    Generate a plot representing how
    statisitcal measures at eqbm change
    as Fconst changes.

    *NOTE* Super ensemble statistical measures
    don't reach eqbm for F < 5.4:

    Either ignore these lower values or 
    switch to single ens runs sfor these
    lower values

'''

import numpy as np
import pickle
from pathlib import Path
import matplotlib.pyplot as plt

savedir = 'plots/eqbm_vals_vs_F/'

# Keys to extract from each pickle file
eqbm_keys = {
    'mean' : 'eqbm_mean',
    'std' : 'eqbm_std',
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
fdir = 'analyzed_data/Fconst/super_ens/'
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


# ============= PLOTTING ==============

# Setting up empty subplots
fig, axs = plt.subplots(nrows=4, ncols=1, figsize=(6,8))

for col, key in enumerate( eqbm_keys ):
    # Plotting model oscillation
    axs[col].scatter(
        F_vals,
        eqbm_vals[key],
        s=10    
    )
# --------------------------\

# Further customizing
axs[0].set_ylabel('Eqbm Mean', fontsize = 16)
axs[1].set_ylabel('Eqbm Std', fontsize = 16)
axs[2].set_ylabel('Eqbm Skew', fontsize = 16)
axs[3].set_ylabel('Eqbm Kurt', fontsize = 16)
axs[3].set_xlabel('F value', fontsize = 19)

for i in range( 4 ):
    axs[i].tick_params(axis='both', labelsize=12)

plt.suptitle('Eqbm Distributions vs F', fontsize = 24)

plt.tight_layout()

# Saving plot
plt.savefig( savedir + 'plot.png' )
plt.close()