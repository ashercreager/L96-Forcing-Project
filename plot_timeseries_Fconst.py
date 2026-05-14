# Packages
import pickle
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# user-settings
savedir = 'plots/Fconst/timeseries/'
loaddir = 'analyzed_data/Fconst/super_ens/'

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
    F = str( data['F'].round(2) )

    # Defining 1d time-array (x-axis)
    time_arr1d = np.arange( 
        0, 
        ( data['num_steps'] ) * data['dt'] ,
        data['dt'],
        dtype='f8'
    )
    
    # Setting up empty subplots
    fig, axs = plt.subplots(nrows=4, ncols=1, figsize=(7,15))

    # MEAN SUBPLOT 
    ax = axs[0]
    ax.set_ylabel( 'RMS Mean', fontsize=19 )
    ax.plot( time_arr1d, data['mean'], '-r', linewidth=2.5)
    ax.axhline( data['eqbm_mean'], color='k', linestyle=':', linewidth=2)

    # STD SUBPLOT 
    ax = axs[1]
    ax.set_ylabel( 'RMS Std', fontsize=19 )
    ax.plot( time_arr1d, data['std'], '-r', linewidth=2.5)
    ax.axhline( data['eqbm_std'], color='k', linestyle=':', linewidth=2)

    # SKEW SUBPLOT 
    ax = axs[2]
    ax.set_ylabel( 'RMS Skew', fontsize=19 )
    ax.plot( time_arr1d, data['skew'], '-r', linewidth=2)
    ax.axhline( data['eqbm_skew'], color='k', linestyle=':', linewidth=2)

    # KURTOSIS SUBPLOT 
    ax = axs[3]
    ax.set_ylabel( 'RMS Kurtosis', fontsize=19 )
    ax.set_xlabel('Model Time (tau)', fontsize=20)
    ax.plot( time_arr1d, data['kurt'], '-r', linewidth=2)
    ax.axhline( data['eqbm_kurt'], color='k', linestyle=':', linewidth=2)


    # CUSTOMIZING
    for subplot in range(4):
        axs[subplot].tick_params(labelsize=15)
    plt.suptitle(f'Ensemble Distribution Time-series', fontsize=25)
    axs[0].set_title(f'F={F}', fontsize=25)
    plt.tight_layout()


    # SAVING
    fname = savedir + f'timeseries_{F}.png'
    plt.savefig( fname )

    plt.close()
    


# Looping over all loaded files and generating
# plots for each of them
for key, data in datadict.items():
    plot( data )

