import numpy as np
import matplotlib.pyplot as plt

# Current forcing runs
forcing_index_1D = np.array( [ 
    6.0, 
    6.5, 
    7.0, 
    7.5, 
    8.0, 
    8.5, 
    9.0, 
    9.5, 
    10.0 
    ] 
)

# note: this process was not done rigorously . . .
# these will all be rather rough approximations 

'''
Times until eqbm
'''

Avg_time_until_stability_1D = np.array( [
    13.75,
    12.6,
    12.85,
    11.0,
    9.0,
    7.8,
    7.5,
    6.85,
    5.4
    ]
)

StdDev_time_until_stability_1D = np.array( [
    11.5,
    11.25,
    11.0,
    8.25,
    8.3,
    7.4,
    7.5,
    5.5,
    5.0
    ] 
)

Skew_time_until_stability_1D = np.array( [
    14.75,
    13.75,
    13.6,
    12.25,
    12.5,
    10.0,
    10.4,
    7.75,
    6.4
    ]
)

Kurtosis_time_until_stability_1D = np.array( [
    10.0,
    11.25,
    12.0,
    8.1,
    10.0,
    7.25,
    7.5,
    5.25,
    5.0
    ]
)

'''
Eqbm values - these values were calculated from the model, not estimated
'''

Eqbm_avg = np.array( [
    2.0,
    2.14,
    2.21,
    2.27,
    2.35,
    2.41,
    2.48,
    2.53,
    2.58
    ]
)

Eqbm_StdDev = np.array( [
    2.8,
    3.03,
    3.24,
    3.45,
    3.64,
    3.83,
    4.01,
    4.20,
    4.37
    ] 
)

Eqbm_Skew = np.array( [
    3.5,
    3.59,
    4.17,
    4.1,
    4.75,
    5.39,
    6.32,
    7.62,
    8.70
    ]
)

Eqbm_Kurtosis = np.array( [
    151,
    206,
    268.8,
    347.54,
    438.0,
    537.08,
    654.0,
    787.8,
    931.5
    ]
)




'''
Plotting
'''

# Init figure
fig, axs = plt.subplots( nrows=4, ncols=2, figsize=(8,9))

# First subplot
ax = axs[0,0]
ax.set_title( 'Time until Ens Avg Eqbm' )
ax.set_ylabel( 'Model Time' )
ax.plot( forcing_index_1D, Avg_time_until_stability_1D, '-r')
#ax.axhline( np.mean(np.sqrt(tseries_sqmean)[-20:]), color='k', linestyle=':')

# 2nd subplot
ax = axs[1,0]
ax.set_title( 'Time until Ens Std Dev Eqbm' )
ax.plot( forcing_index_1D, StdDev_time_until_stability_1D, '-r')

# 3rd subplot
ax = axs[2,0]
ax.set_title( 'Time until Ens Skew Eqbm' )
ax.plot( forcing_index_1D, Skew_time_until_stability_1D, '-r')

# 4th subplot
ax = axs[3,0]
ax.set_title( 'Time until Ens Kurtosis Eqbm' )
ax.set_xlabel('Constant F Value')
ax.plot( forcing_index_1D, Kurtosis_time_until_stability_1D, '-r')

# 5th subplot
ax = axs[0,1]
ax.set_title( 'Eqbm Avg Mean' )
ax.set_ylabel( 'x-value' )
ax.plot( forcing_index_1D, Eqbm_avg, '-b')

# 6th subplot
ax = axs[1,1]
ax.set_title( 'Eqbm Std Dev Mean' )
ax.plot( forcing_index_1D, Eqbm_StdDev, '-b')

# 7th subplot
ax = axs[2,1]
ax.set_title( 'Eqbm Skew Mean' )
ax.plot( forcing_index_1D, Eqbm_Skew, '-b')

# 8th subplot
ax = axs[3,1]
ax.set_title( 'Eqbm Kurtosis Mean' )
ax.set_xlabel( 'Constant F Value' )
ax.plot( forcing_index_1D, Eqbm_Kurtosis, '-b')



plt.tight_layout()

save_directory = './Constant_Forcing_Plots/'
plt.savefig( f'{save_directory}const_forcing_eqbm_time_analysis.png' )