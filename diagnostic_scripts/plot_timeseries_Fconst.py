# Packages
import pickle
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# user-settings
savedir = '../plots/Fconst/timeseries/'
loaddir = '../analyzed_data/Fconst/single_ens/'

# Loading every analyzed_data dict to be plotted
# and saving into a dict containing everything
datadict = {}

fpath = Path(loaddir)

for file in fpath.glob('*.pkl'):
    # Loading pickle file
    fname = loaddir + file.name
    data = pickle.load( open(fname, 'rb') )

    key_name = str( data['F'] )

    # Storing dict inside datadict
    datadict[key_name] = data

# Plotting function
def plot( data ):
    # Input: data dictionary containing
    # all eqbm metrics and cfg settings

    # Defining 1d time-array (x-axis)
    time_arr1d = np.arange( 
        0, 
        ( data['num_steps'] ) * data['dt'] ,
        data['dt'],
        dtype='f8'
    )
    
    # Setting up empty subplots
    fig, axs = plt.subplots(nrows=4, ncols=1, figsize=(6,14))

    # MEAN SUBPLOT 
    ax = axs[0]
    ax.set_title( r'Model Mean', fontsize=16 )
    ax.set_xlabel('')
    ax.plot( time_arr1d, data['mean'], '-r', linewidth=2)
    ax.axhline( data['eqbm_mean'], color='k', linestyle=':', linewidth=2)

    # STD SUBPLOT 
    ax = axs[1]
    ax.set_title( r'Model Std', fontsize=16 )
    ax.set_xlabel('')
    ax.plot( time_arr1d, data['std'], '-r', linewidth=2)
    ax.axhline( data['eqbm_std'], color='k', linestyle=':', linewidth=2)

    # SKEW SUBPLOT 
    ax = axs[2]
    ax.set_title( r'Model Skew', fontsize=16 )
    ax.set_xlabel('')
    ax.plot( time_arr1d, data['skew'], '-r', linewidth=2)
    ax.axhline( data['eqbm_skew'], color='k', linestyle=':', linewidth=2)

    # KURTOSIS SUBPLOT 
    ax = axs[3]
    ax.set_title( r'Model Kurtosis', fontsize=16 )
    ax.set_xlabel('')
    ax.plot( time_arr1d, data['kurt'], '-r', linewidth=2)
    ax.axhline( data['eqbm_kurt'], color='k', linestyle=':', linewidth=2)

    # CUSTOMIZING
    plt.tight_layout()

    # SAVING
    F = str( data['F'] )
    fname = savedir + f'timeseries_{F}.png'
    plt.savefig( fname )

    plt.close()

    print( data['random_seed'] )

plot( datadict['7.0'] )

