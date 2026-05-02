'''
    Script with specified settings
    and plot generation for l96
    under sinusoidal forcing.

    Also contains functionality
    to loop model and plot generation
    for change of parameters.

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
    num_gridpts = 40,      
    num_members   = 4000,  
    tot_num_steps = 10000   #  5840 is 1 year for dt=0.05
)

# Write data on/off
write_eqbm_data = False
write_directory = './Sinusoidal_F/Eqbm_Data/'

# Plot settings
draw_distr_plots = False
draw_tseries_plots = True

plot_save_directory = './Sinusoidal_F/'

# Parameters
amplitude = 2.5
wavelength = (73)  # How long one oscillation should take in model time tau
                 # For seasonal sinusoid, let 1 tau = 5 days =>
                 # dt = 0.05 = ~6 hours
wavelength_dividors = [ 365 ]
div = wavelength_dividors[0]

# In the midlatitudes, winter can experience roughly 50% less
# solar forcing than summers, or something like 30% less forcing 
# from the mean annual forcing.
vshift = 8.5
# Picking F=10.0 to be the mean annual forcing (corresponding
# to findings from constant F runs in which F=10 implied a 
# predictability window of about 2 weeks, which is what we find
# in real world)



''' Needed Objects for Model Loop '''

# Constants
pi = np.pi

runtime = len( wavelength_dividors ) # how many models run

# Functions
def seasonal_forcing( tau ):
    coef = 2 * pi / ( wavelength / div )
    F = amplitude * np.sin( coef * tau ) + vshift
    return F

# NOTE: The current max amplitude is
# F = 11 and F = 6


''' Defining Arrays to Store Data '''

# 2d arrays to store all time series
# arrays of each eqbm metric measured.
# Dimensions = [ Forcing index x time ]
# Arrays will then be filled with model 
# output during loop. Doing it this way 
# serves to avoid use of np.append in
# loop, which isn't a cheap function

time_arr1d = np.arange( 
    0, 
    ( model_settings.tot_num_steps )* 0.0042 ,
    0.0042,
    dtype='f8'
    )

store_tseries_mean_2d = np.zeros(
    (runtime, 
    model_settings.tot_num_steps),
    dtype='f8'
    )
store_tseries_sigma_2d = np.zeros(
    (runtime, 
    model_settings.tot_num_steps),
    dtype='f8'
    )
store_tseries_skew_2d = np.zeros(
    (runtime, 
    model_settings.tot_num_steps),
    dtype='f8'
    )
store_tseries_kurt_2d = np.zeros(
    (runtime, 
    model_settings.tot_num_steps),
    dtype='f8'
    )
store_tseries_forcing_2d = np.zeros(
    (runtime, 
    model_settings.tot_num_steps),
    dtype='f8'
    )


# 1d arrays to store all eqbm final values.
# Dims = [ Findex ]. When writing this data
# to an analysis script, the same element #
# will correspond to the same forcing index
# across all arrays.

store_eqbm_mean_1d = np.zeros( 
    runtime, 
    dtype='f8' 
    ) 
store_eqbm_sigma_1d = np.zeros( 
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
    div = wavelength_dividors[i]
    # MODEL LOOP:
    # Runs l96 model with constant forcing
    # until end of specified runtime (eqbm).
    # During each run, eqbm metrics will be
    # saved for later plotting and analysis.
   
    # RUNS MODEL AND SAVES OUTPUT INTO DICT:
    output_dict = run_model( model_settings, seasonal_forcing )

    # Save time-series output into 2d storage arrays
    store_tseries_mean_2d[i,:] += output_dict.get(
        "tseries_mean_mean"
        )
    store_tseries_sigma_2d[i,:] += output_dict.get(
        "tseries_mean_sigma"
        )
    store_tseries_skew_2d[i,:] += output_dict.get(
        "tseries_mean_skew"
        )
    store_tseries_kurt_2d[i,:] += output_dict.get(
        "tseries_mean_kurt"
        )
    store_tseries_forcing_2d[i,:] += seasonal_forcing( time_arr1d ) 

    # Save final eqbm values into 1d storage arrays
    store_eqbm_mean_1d[i] += output_dict.get(
        "eqbm_mean"
        )
    store_eqbm_sigma_1d[i] += output_dict.get(
        "eqbm_sigma"
        )
    store_eqbm_skew_1d[i] += output_dict.get(
        "eqbm_skew"
        )
    store_eqbm_kurt_1d[i] += output_dict.get(
        "eqbm_kurt"
        )

    # Save all final ens_2d values for later use
    store_final_ens_3d[i,::,::] += output_dict.get( 
        'x_ens2d_final' 
        )

    # Advance loop to next step
    print(f"Model Run Complete . . . ")
#-------------------End Loop


''' Writing Eqbm Data '''

# x_final = store_final_ens_3d[:,:,0]       ==> Code for outputting distribution
# x_final_T = np.transpose(x_final)             of sngle gridpt.
# 
# np.savetxt(
#     f"{write_directory}x_final_{F_start}", 
#     x_final_T, 
#     delimiter=''
#     )

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
    -> Fconst_eqbm_sigmas
    -> Fconst_eqbm_skews
    -> Fconst_eqbm_kurts
    -> Fconst_F_index
    respectively.
    '''

    np.savetxt(
        f"{write_directory}Fconst_eqbm_avgs", 
        store_eqbm_mean_1d, 
        delimiter=","
        )
    np.savetxt(
        f"{write_directory}Fconst_eqbm_sigmas", 
        store_eqbm_sigma_1d, 
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
    gridpt0_distr_plus1 = store_final_ens_3d[i,:,1]

    fig, axs = plt.subplots( nrows=1, ncols=1, figsize=(8, 8) )

    axs.plot( 
        gridpt0_distr,
        gridpt0_distr_plus1,
        linestyle='none',   # want isolated datapoints
        marker='o',         # point marker
        markersize=14.5,
        c='indianred',      # color 
        alpha=0.1
    )

    axs.set_xlabel("x[n]", fontsize=14)
    axs.set_ylabel("x[n+1]", fontsize=14)

    # This function increases font size of axis ticks, just looks nicer
    axs.tick_params(axis='both', which='major', labelsize=12) # Change size for both axes, major ticks

    axs.set_title(f"Final Distribution", fontweight='bold')
    plt.tight_layout()
    freq = np.round( (wavelength / wavelength_dividors[i]) / 73, decimals=3)
    plt.savefig( f'{plot_save_directory}sinuforcing_distr_plot_{freq}_year.png' )

    print(f'Distribution plot drawn . . . ')

zoom_end = 22

def tseries_plotter( i : int):
    # Plots each equilibrium metric wrt 
    # model time per F

    # Init figure
    fig, axs = plt.subplots( nrows=5, ncols=1, figsize=(6,13))

    crests = store_tseries_forcing_2d[ i, : ]
    crest_mask = crests >= 10.996
    peaks_time_1d = time_arr1d[crest_mask]
    leng = len( peaks_time_1d )
    print(leng)

    # 0th subplot
    ax = axs[0]
    ax.set_title( f'Forcing With Time' )
    ax.set_xlabel('')
    ax.set_ylabel('F value')
    ax.plot( time_arr1d, store_tseries_forcing_2d[i,:], '-r')
    for peak in range( leng ):
        ax.axvline(
            peaks_time_1d[peak],
            color='k',
            linestyle=':'
        )
    ax.set_xlim(20,zoom_end)

    # 1st subplot =====================
    ax = axs[1]
    ax.set_title( r'RMS of All Ens Means (all gridpoints)' )
    ax.set_xlabel('')
    ax.plot( time_arr1d, store_tseries_mean_2d[i,:], '-r')
    ax.axhline(
        2.02615, 
        color='lightskyblue', 
        linestyle=':', 
        label='eqbm avg at minimum forcing'
    )
    ax.axhline(
        2.6877, 
        color='crimson', 
        linestyle=':', 
        label='eqbm avg at maximum forcing'
    )
    for peak in range( leng ):
        ax.axvline(
            peaks_time_1d[peak],
            color='k',
            linestyle=':'
        )
    ax.set_ylim(1.6,2.85)
    ax.set_xlim(20,zoom_end)
    ax.legend()

    # 2nd subplot =====================
    ax = axs[2]
    ax.set_title( r'RMS $\sigma$' )
    ax.set_xlabel('')
    ax.plot( time_arr1d, store_tseries_sigma_2d[i,:], '-r')
    ax.axhline(
        2.827, 
        color='lightskyblue', 
        linestyle=':', 
        label='eqbm sigma at minimum forcing'
    )
    ax.axhline(
        4.7214, 
        color='crimson', 
        linestyle=':', 
        label='eqbm sigma at maximum forcing'
    )
    for peak in range( leng ):
        ax.axvline(
            peaks_time_1d[peak],
            color='k',
            linestyle=':'
        )
    ax.set_ylim(2.6,5)
    ax.set_xlim(20,zoom_end)
    ax.legend()


    # 3rd subplot =====================
    ax = axs[3]
    ax.set_title( r'RMS of All Ens Skews' )
    ax.set_xlabel('')
    ax.plot( time_arr1d, store_tseries_skew_2d[i,:], '-r')
    for peak in range( leng ):
        ax.axvline(
            peaks_time_1d[peak],
            color='k',
            linestyle=':'
        )
    ax.axhline(
        0.1228, 
        color='lightskyblue', 
        linestyle=':', 
        label='eqbm skew at minimum forcing'
    )
    ax.axhline(
        0.10352, 
        color='crimson', 
        linestyle=':', 
        label='eqbm skew at maximum forcing'
    )
    ax.set_xlim(20,zoom_end)
    ax.set_ylim(0.07,0.15)
    ax.legend()


    # 4th subplot =====================
    ax = axs[4]
    ax.set_title( r'RMS of All Ens Kurtosis' )
    ax.set_xlabel('Model Time', fontsize=12)
    ax.plot( time_arr1d, store_tseries_kurt_2d[i,:], '-r')
    for peak in range( leng ):
        ax.axvline(
            peaks_time_1d[peak],
            color='k',
            linestyle=':'
        )
    ax.axhline(
        0.61754, 
        color='lightskyblue', 
        linestyle=':', 
        label='eqbm kurt at minimum forcing'
    )
    ax.axhline(
        0.42938, 
        color='crimson', 
        linestyle=':', 
        label='eqbm kurt at maximum forcing'
    )
    ax.set_xlim(20,zoom_end)
    ax.set_ylim(0.2, 0.8)
    ax.legend()


    
    plt.tight_layout()
    freq = np.round( (wavelength / wavelength_dividors[i]) / 73, decimals=3)
    plt.savefig( f'{plot_save_directory}sinuforcing_tseries_plot_zoomed_diurnal.png' )

    print(f'Timeseries plot drawn . . . ')


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