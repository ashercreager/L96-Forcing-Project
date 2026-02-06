''' 
    Generate an ensemble under constant forcing.

    # Note: Equilibrated ensembles should only exist for 
            situations with constant forcing F
'''

import numpy as np
from math import exp
import matplotlib.pyplot as plt
import lorenz96_model as l96


'''
    User settings
'''

# Plot output
plot_type = "statplot" # can be a "statplot", "scatterplot", "gridplot", "none"

# Plot save directory
save_directory = './Const_F/Const_F_Plots/'

# Save names
statplotname = "Fconst_eqbm_metrics_"
scatplotname = "Fconst_eqbm_scatter_"
gridplotname = "Fconst_eqbm_grdpt_plot_"

# Eqbm data save directory
eqbm_data_save_directory = "./Const_F/Equilibrium_Data/"

# Boolean to write data or not
write_data = False

# Number of elements on a 'latitude' ring
num_gridpts = 40

# Number of ensemble members
num_ens = 4000

# Total number of steps to run ensemble for
# dt = 0.05 means total_simulation_runtime = tot_num_steps * 0.05
tot_num_steps = 300 

# Constant forcing function
Fstart = 6.0
Fstop = 6.0
Finterval = 0.5
Fconst = Fstart * 1
def constant_forcing_F( tau ):
    return Fconst







'''
    Preparing different arrays to hold data 
'''

# Empty arrays to store stat measures at each time interval of the simulation (aka equilibration metrics)
tseries_sqmean = np.zeros( tot_num_steps, dtype='f8' )
tseries_sigma2 = np.zeros( tot_num_steps, dtype='f8' )
tseries_sqskew = np.zeros( tot_num_steps, dtype='f8' )
tseries_sqkurt = np.zeros( tot_num_steps, dtype='f8' )

# Prepping empty arrays to hold eqbm value data
store_avg_eqbm_vals_1d      = np.array( [] )
store_std_dev_vals_eqbm_1d  = np.array( [] )
store_skew_vals_eqbm_1d     = np.array( [] )
store_kurt_vals_eqbm_1d     = np.array( [] )



# Time array for the equilibration metric plots
time_arr1d = np.arange( tot_num_steps ) * l96.dt

# 2D Gridpoint index for the gridpoint plot
gridpt_index_1D = np.arange(1,num_gridpts+1)

gridpt_index_2D = np.tile(  # Function to create a higher dimensional array by repeating - 'tiling' - another
    gridpt_index_1D,        # --> The array being tiled
    ( num_ens, 1 )          # () # of rows tiling, how many times copied horizontally )
) 





'''
    Run simulation and plot generation loop
'''

# Loops until all simulation runs are done
while Fconst <= Fstop:


    # Reset stat arrays
    tseries_sqmean *= 0
    tseries_sigma2 *= 0
    tseries_sqskew *= 0
    tseries_sqkurt *= 0



    ''' Prep an ensemble of initial model states '''
    # Ensuring that the same random seed is used each simulation for reproducibility 
    np.random.seed(0)

    # Prep a reference state using the desired forcing
    x_single = np.random.normal( loc=0, scale=1e-1, size=(1, num_gridpts) )

    # Spin-up that reference state
    x_single, _ = l96.multistep( 
        x_single, 0, constant_forcing_F, 1000
    )

    # Sample from random noise
    x_ens2d_init = x_single + np.random.normal( loc=0, scale=1e-2, size=(num_ens, num_gridpts) )
    # What this above is doing is adding tiny perturbations to the reference ensemble
    # for every single extra ensemble being ran. 



    ''' Running Simulation '''

    # Define x_ens2d before first simulation run
    x_ens2d = x_ens2d_init * 1

    # Run simulation.
    tau = 0.
    for i in range( tot_num_steps ):

        # Advance state
        x_ens2d, tau = l96.multistep( 
            x_ens2d, tau, constant_forcing_F, 1 
        )



        ''' Computing eqbm metrics at each time-step '''

        # average state
        x_avg = np.mean( x_ens2d, axis=0 )

        # Compute equilibration metrics
        tseries_sqmean[i] = np.mean( 
            np.mean( x_ens2d, axis=0)**2
        )
        tseries_sigma2[i] = np.mean( 
            np.var( x_ens2d, axis=0, ddof=1 )
        )
        tseries_sqskew[i] = np.mean( 
            np.power(
                np.mean( np.power(x_ens2d - x_avg, 3), axis=0 )
                , 2 # not true skew, actually 3rd central moment, turn into true skew
            )
        )
        tseries_sqkurt[i] = np.mean( 
            np.power(
                np.mean( np.power(x_ens2d - x_avg, 4), axis=0 )
                , 2 # not true kurt, actually 4th moment, turn into true kurt (and learn what means)
            )
        )

        #########################
    # ---- End of simulation loop



    ''' Compiling Eqbm Values for writing data later'''

    # Approximate value where the ens avg is stable
    ens_avg_eqbm_val = np.mean(np.sqrt(tseries_sqmean)[-20:])
    
    # Approximate value where ens std dev is stable
    ens_std_dev_eqbm_val = np.mean(np.sqrt(tseries_sigma2)[-20:])

    # Approximate value where ens skew is stable
    ens_skew_eqbm_val = np.mean(np.sqrt(tseries_sqskew)[-20:])

    # Approximate value where kurtosis is stable
    ens_kurtosis_eqbm_value = np.mean(np.sqrt(tseries_sqkurt)[-20:])

    # Appending eqbm values to their respective 'storing' arrays
    store_avg_eqbm_vals_1d = np.append(
        store_avg_eqbm_vals_1d,
        [ens_avg_eqbm_val]
    )

    store_std_dev_vals_eqbm_1d = np.append(
        store_std_dev_vals_eqbm_1d,
        [ens_std_dev_eqbm_val]
    )

    store_skew_vals_eqbm_1d = np.append(
        store_skew_vals_eqbm_1d,
        [ens_skew_eqbm_val]
    )

    store_kurt_vals_eqbm_1d = np.append(
        store_kurt_vals_eqbm_1d,
        [ens_kurtosis_eqbm_value]
    )




    ''' Drawing desired plots for each run'''

    if plot_type == "statplot":
        ### Plots each equilibrium metric wrt model time

        # Init figure
        fig, axs = plt.subplots( nrows=4, ncols=1, figsize=(4,9))

        # 1st subplot =====================
        ax = axs[0]
        ax.set_title( 'RMS of Ens Avg' )
        ax.set_xlabel('')
        ax.plot( time_arr1d, np.sqrt(tseries_sqmean), '-r')
        ax.axhline( ens_avg_eqbm_val, color='k', linestyle=':')

        
        #note: make this save info to some kind of doc

        # 2nd subplot =====================
        ax = axs[1]
        ax.set_title( 'RMS of Ens Std Dev' )
        ax.set_xlabel('')
        ax.plot( time_arr1d, np.sqrt(tseries_sigma2), '-r')
        ax.axhline( ens_std_dev_eqbm_val, color='k', linestyle=':')


        # 3rd subplot =====================
        ax = axs[2]
        ax.set_title( 'RMS of Ens Skew' )
        ax.set_xlabel('')
        ax.plot( time_arr1d, np.sqrt(tseries_sqskew), '-r')
        ax.axhline( ens_skew_eqbm_val, color='k', linestyle=':')


        # 4th subplot =====================
        ax = axs[3]
        ax.set_title( 'RMS of Ens Kurtosis' )
        ax.set_xlabel('Model Time')
        ax.plot( time_arr1d, np.sqrt(tseries_sqkurt), '-r')
        ax.axhline( ens_kurtosis_eqbm_value, color='k', linestyle=':')

        plt.tight_layout()

        plt.savefig( f'{save_directory}{statplotname}{Fconst}.png' )


    elif plot_type == "scatterplot":
        ### Plots the final eqbm distribution of a single gridpoint in n vs n+1 form

        # Recollecting x_ens2d ensemble data for only 1 gridpoint
        ens_collection_grdpt0 = x_ens2d[0::, 0:1]

        # Sliding all elements of ens_collection 1 index to plot (x_n, x_n+1)
        ens_collection_plus1_grdpt0 = np.append(
            ens_collection_grdpt0[1::],             # Element 1 new start of array
            ens_collection_grdpt0[0]                # Puts n=0 at end
        )   


        plt.figure(figsize=(8, 8))
        # Inputting two 2D arrays of the same dimensions will 
        # plot the values of both respective arrays at the same
        # index.
        plt.plot( 
            ens_collection_grdpt0,
            ens_collection_plus1_grdpt0,
            linestyle='none',   # want isolated datapoints
            marker='o',         # point marker
            markersize=4,
            c='indianred',      # color 
            alpha=1.0
        )

        plt.xlabel("x[n]")
        plt.ylabel("x[n+1]")
        plt.title(f"Eqbm Distribution for constant F={Fconst}", fontweight='bold')
        plt.tight_layout()


        plt.savefig( f'{save_directory}{scatplotname}{Fconst}.png' )


    elif plot_type == "gridplot":
        ### Plots the final eqbm distribution across all gridpoint for every ensemble     

        plt.figure(figsize=(9, 7))

        # Inputting two 2D arrays of the same dimensions will plot
        # the values of both respective arrays at the same index.
        plt.plot( 
            gridpt_index_2D,
            x_ens2d,
            linestyle='none',   # want isolated datapoints
            marker='.',         # point marker
            markersize=3,
            c='r',              # color red
            alpha=1.0
        )

        plt.xlabel("Gridpoints")
        plt.ylabel("Final x value")
        plt.title(f"Eqbm Distribution for constant F={Fconst}")
        plt.tight_layout()


        plt.savefig( f'{save_directory}{gridplotname}{Fconst}.png' )

        
    else:
        ### In case of a typo
        print("No plots drawn")

    # ---------- End of plot generation code


    # End of loop necessaries
    Fconst += Finterval
        

    ##########################################
# ----------------------------------- End Loop






'''
    Writing eqbm value data to a text file to be stored
'''

if write_data == True:

    # Forcing index for each model run
    const_F_vals_1d = np.arange( Fstart, Fstop + Finterval, Finterval )

    # Data arrays will have the following pattern:
    # Elements [0,2,4,...] representing consecutive F
    # Elements [1,3,5,...] representing eqbm metric values
    #
    # Therefore, each eqbm value array should have twice 
    # as many total elements as # of simulations ram
    data_arr_length = 2 * len(const_F_vals_1d)

    # Prepping empty arrays to hold eqbm value data with adjacent forcing index
    all_avg_eqbm_data_1d      = np.zeros( data_arr_length, dtype='f8' )
    all_std_dev_eqbm_data_1d  = np.zeros( data_arr_length, dtype='f8' )
    all_skew_eqbm_data_1d     = np.zeros( data_arr_length, dtype='f8' )
    all_kurt_eqbm_data_1d     = np.zeros( data_arr_length, dtype='f8' )

    # Compile data into arrays following this format:
    # 
    # Elements [0,2,4,...] represent consecutive F
    # Elements [1,3,5,...] represent eqbm metric values
    
    all_avg_eqbm_data_1d[0::2] += const_F_vals_1d
    all_avg_eqbm_data_1d[1::2] +=  store_avg_eqbm_vals_1d

    all_std_dev_eqbm_data_1d[0::2] += const_F_vals_1d
    all_std_dev_eqbm_data_1d[1::2] += store_std_dev_vals_eqbm_1d

    all_skew_eqbm_data_1d[0::2] += const_F_vals_1d
    all_skew_eqbm_data_1d[1::2] += store_skew_vals_eqbm_1d

    all_kurt_eqbm_data_1d[0::2] += const_F_vals_1d
    all_kurt_eqbm_data_1d[1::2] += store_kurt_vals_eqbm_1d

    # Writing data to csv file
    np.savetxt(
        f"{eqbm_data_save_directory}const_F_avg_eqbm_values", 
        all_avg_eqbm_data_1d, 
        delimiter=","
        )

    np.savetxt(
        f"{eqbm_data_save_directory}const_F_std_dev_eqbm_values", 
        all_std_dev_eqbm_data_1d, 
        delimiter=","
        )

    np.savetxt(
        f"{eqbm_data_save_directory}const_F_skew_eqbm_values", 
        all_skew_eqbm_data_1d, 
        delimiter=","
        )

    np.savetxt(
        f"{eqbm_data_save_directory}const_F_kurt_eqbm_values", 
        all_kurt_eqbm_data_1d, 
        delimiter=","
        )
    
else:
        print( "No eqbm data written" )





quit()