import numpy as np
import matplotlib.pyplot as plt

'''
    User Settings
'''

plot_color = 'cornflowerblue'


'''
Eqbm values - these values were calculated from the model, not estimated
'''

Eqbm_Avgs_1d    = np.loadtxt("./Eqbm_Data/Fconst_eqbm_avgs")

Eqbm_StdDevs_1d =  np.loadtxt("./Eqbm_Data/Fconst_eqbm_sigmas")

Eqbm_Skews_1d   = np.loadtxt("./Eqbm_Data/Fconst_eqbm_skews")

Eqbm_Kurts_1d   = np.loadtxt("./Eqbm_Data/Fconst_eqbm_kurts")

F_index_1D = np.loadtxt("./Eqbm_Data/Fconst_F_index")

'''
Plotting
'''

# Init figure
fig, axs = plt.subplots( nrows=4, ncols=1, figsize=(4,9))


# 1st subplot
ax = axs[0]
ax.set_title( 'Eqbm Avg Mean' )
ax.set_ylabel( 'x-value' )
ax.plot( F_index_1D, Eqbm_Avgs_1d, c=plot_color)

# 2nd subplot
ax = axs[1]
ax.set_title( 'Eqbm Std Dev Mean' )
ax.plot( F_index_1D, Eqbm_StdDevs_1d, c=plot_color)

# 3rd subplot
ax = axs[2]
ax.set_title( 'Eqbm Skew Mean' )
ax.plot( F_index_1D, Eqbm_Skews_1d, c=plot_color)

# 4th subplot
ax = axs[3]
ax.set_title( 'Eqbm Kurtosis Mean' )
ax.set_xlabel( 'Constant F Value' )
ax.plot( F_index_1D, Eqbm_Kurts_1d, c=plot_color)

plt.tight_layout()

save_directory = './Plots/'
plt.savefig( f'{save_directory}Fconst_eqbm_metric_analysis.png' )

print('Analysis plot successfuly drawn!')