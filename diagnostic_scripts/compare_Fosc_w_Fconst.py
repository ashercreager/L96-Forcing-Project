'''

    This script plots/compares Fosc
    to what the Fconst eqbm values
    would be at each point for that
    given forcing

'''

# packages
import numpy as np
import pickle
from pathlib import Path
import matplotlib.pyplot as plt

# user-settings
savedir = '../plots/Fosc_vs_Feqbm/'

# ============ LOADING DATA ================

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

#  ========== DETERMINING EQBM-OSC ===========
# Creating a timeseries dict to represent Fosc
# if it reached its Fconst eqbm values at every
# forcing value

# Initializing
eqbm_osc = {}

# Filling eqbm_osc
for key in eqbm_keys:

    # Initializing a timeseries array for given metric
    eqbm_osc[ key ] = np.zeros( Fosc['num_steps'] )

    for indx, F in enumerate( F_vals ):
        # Checking which F values in Fosc
        # are closest to the Fconst values
        # that data exists for and then filling
        diff = np.abs( Fosc['F_tseries'] - F )
        mask = ( diff <= .05 )

        eqbm_osc[ key ][ mask ] = eqbm_vals[ key ][ indx ]

    # Replacing all intermediary F-vals (those which no we don't
    # have data for) with nans
    mask = ( eqbm_osc[ key ] == 0.0 )
    eqbm_osc[ key ][ mask ] = np.nan


# ============= PLOTTING ==============

# Defining 1d time-array (x-axis)
time_arr1d = np.arange( 
    0, 
    ( Fosc['num_steps'] ) * Fosc['dt'] ,
    Fosc['dt'],
    dtype='f8'
)

# Setting up empty subplots
fig, axs = plt.subplots(nrows=2, ncols=4, figsize=(20,8))

# First plotting F timeseries
for col in range(4):
    axs[0,col].plot( time_arr1d, Fosc['F_tseries'], '-b', linewidth=3 )
    axs[0,col].set_ylim(5.0,13.0)
# --------------------------\

# Next plotting Fosc overlaid w/ eqbm_osc for each
# metric
for col, key in enumerate( eqbm_keys ):
    # Plotting model oscillation
    axs[1,col].plot(
        time_arr1d,
        Fosc[ key ], 
        '-r',
        label=f'Model {key}',
        linewidth=3
    )

    # Plotting eqbm oscillation
    axs[1,col].plot(
        time_arr1d,
        eqbm_osc[ key ],
        'black',
        label=f'Eqbm osc {key}'
    )

    # Customizing
    axs[1,col].set_ylabel('Mean', fontsize = 18)
    axs[1,col].set_xlabel('Model Time (tau)', fontsize = 18)
    axs[1,col].legend(fontsize=15) 
# --------------------------\

# Defining window limits
for row in range(2):
    for col in range(4):
        axs[row,col].set_xlim(10,100)

        if row == 1:
            key = list(eqbm_keys)[col]

            minlim = np.nanmin(
                Fosc[key][100:]
            ) - 0.2

            maxlim = np.nanmax(
                Fosc[key][100:]
            ) + 0.2

            axs[row,col].set_ylim(minlim,maxlim)
# --------------------------\


# fig.suptitle('', fontsize=20)
plt.tight_layout()

# Saving plot
plt.savefig( savedir + 'test.png' )
plt.close()