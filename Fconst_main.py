'''
    Script with specified settings
    and plot generation for l96
    under constant forcing.

    Also contains functionality
    to loop model and plot generation
    for consecutively increasing 
    values of F.

    Allows for writing equilibrium 
    data to a text file for later
    analysis.
'''

# Packages
from run_lorenz96 import config, run_model
import numpy as np
import matplotlib.pyplot as plt

'''     User Settings       '''

model_settings = config(
    num_gridpts = 40,       # 40 gridpts is the norm
    num_members    = 9000,  # increased members for more accurate distribution
    tot_num_steps  = 340    # increased number of steps, early runs nots in eqbm
)

# F Settings for looped runs
F_start = 6.0
F_end   = 11.0
F_step  = 0.125

# Write data on/off
write_eqbm_data = True
write_directory = './Const_F/Eqbm_Data/'

# Plot settings
draw_distr_plots = True
draw_tseries_plots = True

plot_save_directory = './Const_F/Plots/'

''' Needed Objects for Model Loop '''

# Calculating the # of iterations to run model.
# Rounding ensures no float values break the 
# loop. + 1 is necessary as F_end is inclusive.
# Note: runtime = (# of models ran) 
runtime : int = round( ( F_end - F_start ) / F_step ) + 1

# Defining Constant Forcing Function
F = F_start # F initially at start value

def const_forcing( tau ):
    return F


''' Defining Empty Arrays to Store Data '''

# 2d arrays to store all time series
# arrays of each eqbm metric measured.
# Dimensions = [ Forcing index x time ]
# Arrays will then be filled with model 
# output during loop. Doing it this way 
# serves to avoid use of np.append in
# loop, which isn't a cheap function

store_tseries_sqmean_2d = np.zeros(
    (runtime, 
    model_settings.tot_num_steps),
    dtype='f8'
    )
store_tseries_sigma2_2d = np.zeros(
    (runtime, 
    model_settings.tot_num_steps),
    dtype='f8'
    )
store_tseries_sqskew_2d = np.zeros(
    (runtime, 
    model_settings.tot_num_steps),
    dtype='f8'
    )
store_tseries_sqkurt_2d = np.zeros(
    (runtime, 
    model_settings.tot_num_steps),
    dtype='f8'
    )
store_tseries_Findex_2d = np.zeros(
    (runtime, 
    model_settings.tot_num_steps),
    dtype='f8'
    )

# 1d arrays to store all eqbm final values.
# Dims = [ Findex ]. When writing this data
# to an analysis script, the same element #
# will correspond to the same forcing index
# across all arrays.

store_eqbm_sqmean_1d = np.zeros( 
    runtime, 
    dtype='f8' 
    ) 
store_eqbm_sigma2_1d = np.zeros( 
    runtime, 
    dtype='f8' 
    ) 
store_eqbm_skew_1d   = np.zeros( 
    runtime, 
    dtype='f8' 
    )
store_eqbm_kurt_1d   = np.zeros( 
    runtime, 
    dtype='f8' 
    )

store_eqbm_Findex_1d = np.zeros( 
    runtime, 
    dtype='f8' 
    )

# 3d array to store ens_2d values from
# each model run.
# Dims = [ Findex, member #, gridpt]

store_final_ens_3d = np.zeros( 
    (runtime, 
    model_settings.num_members,
    model_settings.num_gridpts),
    dtype='f8' 
    )


''' Running Model Loop '''

for i in range(runtime):
    # MODEL LOOP:
    # Runs l96 model with constant forcing
    # until end of specified runtime (eqbm).
    # During each run, eqbm metrics will be
    # saved for later plotting and analysis.
   
    # RUNS MODEL AND SAVES OUTPUT INTO DICT:
    output_dict = run_model( model_settings, const_forcing )

    # Save time-series output into 2d storage arrays
    store_tseries_sqmean_2d[i,:] += output_dict.get(
        "tseries_sqmean"
        )
    store_tseries_sigma2_2d[i,:] += output_dict.get(
        "tseries_sigma2"
        )
    store_tseries_sqskew_2d[i,:] += output_dict.get(
        "tseries_sqskew"
        )
    store_tseries_sqkurt_2d[i,:] += output_dict.get(
        "tseries_sqkurt"
        )
    store_tseries_Findex_2d[i,:] += F

    # Save final eqbm values into 1d storage arrays
    store_eqbm_sqmean_1d[i] += output_dict.get(
        "eqbm_avg"
        )
    store_eqbm_sigma2_1d[i] += output_dict.get(
        "eqbm_std"
        )
    store_eqbm_skew_1d[i] += output_dict.get(
        "eqbm_skew"
        )
    store_eqbm_kurt_1d[i] += output_dict.get(
        "eqbm_kurt"
        )
    store_eqbm_Findex_1d[i] += F

    # Save all final ens_2d values for later use
    store_final_ens_3d[i,::,::] += output_dict.get( 
        'x_ens2d_final' 
        )

    # Advance loop to next step
    print(f"F = {F} Model Run Complete . . . ")
    F += F_step
#-------------------End Loop


''' Writing Eqbm Data '''

if write_eqbm_data == True:
    # If true, all eqbm data will be
    # written to their respective txt
    # files to be read by other scripts.

    # NOTE: EACH TIME THIS IS CALLED, THE 
    # PREVIOUSLY WRITTEN DATA WILL BE OVERWRITTEN.
    
    # This shouldn't really matter 
    # this project as it currently 
    # is, as the model is perfectly 
    # reproducible and I'll be running
    # mostly the same settings.

    # Data gets written using np.savetxt function

    '''
    File save names given by:
    -> Fconst_eqbm_avgs
    -> Fconst_eqbm_sigma2s
    -> Fconst_eqbm_skews
    -> Fconst_eqbm_kurts
    -> Fconst_F_index
    respectively.
    '''

    np.savetxt(
        f"{write_directory}Fconst_F_index", 
        store_eqbm_Findex_1d, 
        delimiter=","
        )
    np.savetxt(
        f"{write_directory}Fconst_eqbm_avgs", 
        store_eqbm_sqmean_1d, 
        delimiter=","
        )
    np.savetxt(
        f"{write_directory}Fconst_eqbm_sigma2s", 
        store_eqbm_sigma2_1d, 
        delimiter=","
        )
    np.savetxt(
        f"{write_directory}Fconst_eqbm_skews", 
        store_eqbm_skew_1d, 
        delimiter=","
        )
    np.savetxt(
        f"{write_directory}Fconst_eqbm_kurts", 
        store_eqbm_kurt_1d, 
        delimiter=","
        )
        
    print("All eqbm data written")


''' Setting Up Plots '''

def distr_plotter( i : int ):  
    # Plots the final eqbm distribution
    # of all ensemble members of a single 
    # gridpoint in n vs n+1 form.

    # Paramter 'i' indicates forcing number

    # Collecting final x_ens2d ensemble data 
    # for only gridpoint 0, given some forcing F
    gridpt0_distr = store_final_ens_3d[ i, :, 0 ]

    # Sliding all elements of ens_collection 1 index over (x_n+1)
    gridpt0_distr_plus1 = np.append(
        gridpt0_distr[1::],    # -> Element 1 new start of array
        gridpt0_distr[0]       # -> Puts n=0 at end
    )   

    fig, axs = plt.subplots( nrows=1, ncols=1, figsize=(8, 8) )

    axs.plot( 
        gridpt0_distr,
        gridpt0_distr_plus1,
        linestyle='none',   # want isolated datapoints
        marker='o',         # point marker
        markersize=4,
        c='indianred',      # color 
        alpha=1.0
    )

    axs.set_xlabel("x[n]", fontsize=14)
    axs.set_ylabel("x[n+1]", fontsize=14)

    # This function increases font size of axis ticks, just looks nicer
    axs.tick_params(axis='both', which='major', labelsize=12) # Change size for both axes, major ticks

    Fnum = i * F_step + F_start
    axs.set_title(f"Eqbm Distribution for constant F={Fnum}", fontweight='bold')
    plt.tight_layout()
    plt.savefig( f'{plot_save_directory}Fconst_distr_plot_{Fnum}.png' )

    print(f'Distribution plot drawn for F = {Fnum} . . . ')

time_arr1d = np.arange( 
    0, 
    ( model_settings.tot_num_steps )* 0.05 ,
    0.05,
    dtype='f8'
    )

def tseries_plotter( i : int):
    # Plots each equilibrium metric wrt 
    # model time per F

    # Init figure
    fig, axs = plt.subplots( nrows=4, ncols=1, figsize=(4,9))

    # 1st subplot =====================
    ax = axs[0]
    ax.set_title( 'RMS of Ens Avg' )
    ax.set_xlabel('')
    ax.plot( time_arr1d, np.sqrt(store_tseries_sqmean_2d[i,:]), '-r')
    ax.axhline( store_eqbm_sqmean_1d[i], color='k', linestyle=':')
    
    #note: make this save info to some kind of doc
    # 2nd subplot =====================
    ax = axs[1]
    ax.set_title( 'RMS of Ens Std Dev' )
    ax.set_xlabel('')
    ax.plot( time_arr1d, np.sqrt(store_tseries_sigma2_2d[i,:]), '-r')
    ax.axhline( store_eqbm_sigma2_1d[i], color='k', linestyle=':')
    # 3rd subplot =====================
    ax = axs[2]
    ax.set_title( 'RMS of Ens Skew' )
    ax.set_xlabel('')
    ax.plot( time_arr1d, np.sqrt(store_tseries_sqskew_2d[i,:]), '-r')
    ax.axhline( store_eqbm_skew_1d[i], color='k', linestyle=':')
    # 4th subplot =====================
    ax = axs[3]
    ax.set_title( 'RMS of Ens Kurtosis' )
    ax.set_xlabel('Model Time', fontsize=12)
    ax.plot( time_arr1d, np.sqrt(store_tseries_sqkurt_2d[i,:]), '-r')
    ax.axhline( store_eqbm_kurt_1d[i], color='k', linestyle=':')
    
    Fnum = i * F_step + F_start

    plt.tight_layout()
    plt.savefig( f'{plot_save_directory}Fconst_tseries_plot_{Fnum}.png' )

    print(f'Timeseries plot drawn for F = {Fnum} . . . ')


''' Drawing-Plot Loop '''

if draw_distr_plots == True:
    # Loop plot-generation for all F-runs
    for i in range( runtime ):
        distr_plotter(i)

if draw_tseries_plots == True:
    # Loop plot-generation for all F-runs
    for i in range( runtime ):
        tseries_plotter(i)


# --- END SCRIPT ---
print('Complete!')