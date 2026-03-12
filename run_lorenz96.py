'''
    This script contains the main functions
    necessary to run the lorenz96 model once
    on an entire ensemble across a discretized 
    latitude circle. Forcing F can be a constant 
    or spatially/temporally variable function.

    Equilibrium metrics are also calculated 
    during each timestep during the model run
    for future plotting and analysis.

    # Note: Equilibrated ensembles 
    should only exist for situations
    with constant forcing F
'''


# Packages
import numpy as np
import matplotlib.pyplot as plt
import lorenz96_model as l96
from math import exp

from dataclasses import dataclass


@dataclass
class config:
    # Model configuration settings
    num_gridpts : int = 40 
    num_members : int = 4000  # ens members
    tot_num_steps : int = 300 # how long should the model run  
    # note: total runtime in model time
    # = dt * tot_num_steps ; dt = 0.05


# Defining Functions
def init_ensemble( cfg: config, forcing_func ):
    ''' Generates an initial-state (tau = 0) ensemble 
        of slightly perturbed members from a single
        reference member  
    '''
    # For reproducibility, reset random seed each call
    np.random.seed(0)

    # Define the ensemble member which all other members will be perturbed from (reference member)
    x_single = np.random.normal( loc=0, scale=1e-1, size=(1, cfg.num_gridpts) )

    # Let l96 run for 1000 steps on reference state so it attains model-accurate values
    x_single, _ = l96.multistep( x_single, 0, forcing_func, 2000 ) # mess with last param a little

    # Create the 2d ensemble array of slightly perturbed members from the reference state
    x_ens2d_init = x_single + np.random.normal( loc=0, scale=1e-2, size=(cfg.num_members, cfg.num_gridpts) )
    return x_ens2d_init


def compute_eqbm_metrics( x_ens2d, n ):
    ''' Function to compute each of the eqbm metrics 
        (ensemble average, std dev, skew, kurt) during
        any given timestep of the simulation

        NOTE: this currently computes the eqbm
        metrics of all member across every 
        gridpoint seperately, and then RMS's
        them to find the 'mean model' magnitudes

        input n is the number of members being ran:
        used to represent the number of samples per
        gridpoint. Grabbed from cfg (num_members)
    '''

    # Computing the averages of each gridpt
    # and then storing in a 1d array.
    gridpt_means_1d = np.mean( x_ens2d, axis=0 )

    # Computing central moments of each gridpt
    moment2_1d = ( 1/n ) * np.sum( (x_ens2d - gridpt_means_1d)**2, axis=0 ) # 2nd central moment
    moment3_1d = ( 1/n ) * np.sum( (x_ens2d - gridpt_means_1d)**3, axis=0 ) # 3rd central moment
    moment4_1d = ( 1/n ) * np.sum( (x_ens2d - gridpt_means_1d)**4, axis=0 ) # 4th central moment

    # Computing standard deviations of each gridpt
    sigmas_1d = np.sqrt( moment2_1d )

    # Computing skewness of each gridpt
    skews_1d = moment3_1d / ( sigmas_1d**3 )

    # Computing (excess) kurtosis of each gridpt
    kurts_1d = moment4_1d / ( sigmas_1d**4 ) - 3.0

    # Everything above has calculated the eqbm
    # metrics of every gridpt and stored them
    # into their resp. 1d arrays. The following
    # code is meant to take the root-mean-square
    # of each of these metric across the entire
    # latitude circle to find the magnitudes of 
    # the 'model-average' mean state, sigma, skew,
    # and kurtosis.
    #
    # Basically asking, "at a random gridpoint,
    # what is the magnitude of the typical 
    # ensemble mean state/sigma/skew/kurtosis?"
    #
    # If all four have stabilized with time, 
    # then the model's distribution is no longer
    # changing signficantly with time and has
    # essentially reached 'peak randomness'

    model_mean  = np.sqrt( np.mean( gridpt_means_1d ** 2 ) )
    model_sigma = np.sqrt( np.mean( sigmas_1d ** 2 ) )
    model_skew = np.sqrt( np.mean( skews_1d ** 2 ) )
    model_kurt = np.sqrt( np.mean( kurts_1d ** 2 ) )

    return model_mean, model_sigma, model_skew, model_kurt



def run_model( cfg: config, forcing_func ):
    ''' Function to run l96 model to a specified
        number of steps on the entire ensemble
    '''

    # Defining empty arrays to store equilibration metrics at each time step
    tseries_mean_mean = np.zeros( cfg.tot_num_steps, dtype='f8' )
    tseries_mean_sigma = np.zeros( cfg.tot_num_steps, dtype='f8' )
    tseries_mean_skew = np.zeros( cfg.tot_num_steps, dtype='f8' )
    tseries_mean_kurt = np.zeros( cfg.tot_num_steps, dtype='f8' )

    # Define x_ens2d before first simulation run
    x_ens2d = init_ensemble( cfg, forcing_func )

    # Loop model over n consecutive steps
    tau = 0.
    for i in range( cfg.tot_num_steps ):

        # Advance state
        x_ens2d, tau = l96.multistep( 
            x_ens2d, tau, forcing_func, 1 
        )

        # Solving eqbm metrics at each timestep
        (tseries_mean_mean[i], 
         tseries_mean_sigma[i], 
         tseries_mean_skew[i], 
         tseries_mean_kurt[i]) = compute_eqbm_metrics ( x_ens2d, cfg.num_members )
    # ------------End loop


    # Calculating final values to which eqbm metrics are stable.
    # Note: These assume that each eqbm metric stabilizes by the
    # last 20 steps of the model

    # Approximate value where the ens avg is stable
    eqbm_mean = np.mean(tseries_mean_mean[-20:])
    
    # Approximate value where ens std dev is stable
    eqbm_sigma = np.mean(tseries_mean_sigma[-20:])

    # Approximate value where ens skew is stable
    eqbm_skew = np.mean(tseries_mean_skew[-20:])

    # Approximate value where kurtosis is stable
    eqbm_kurt = np.mean(tseries_mean_kurt[-20:])

    # Output
    return {
        "tseries_mean_mean" : tseries_mean_mean,    # 1D array type
        "tseries_mean_sigma": tseries_mean_sigma,   # 1D array type
        "tseries_mean_skew" : tseries_mean_skew,    # 1D array type
        "tseries_mean_kurt" : tseries_mean_kurt,    # 1D array type
        
        "eqbm_mean"  : eqbm_mean,   # Float type
        "eqbm_sigma" : eqbm_sigma,  # Float type
        "eqbm_skew"  : eqbm_skew,   # Float type
        "eqbm_kurt"  : eqbm_kurt,   # Float type

        "x_ens2d_final" : x_ens2d,              # 2d array type: [ member #, gridpt # ]
    }
    
