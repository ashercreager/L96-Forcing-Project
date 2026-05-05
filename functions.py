'''

    A script to contain general functions needed
    throughout this project

'''

# packages
import numpy as np

def compute_eqbm_metrics( x3d, num_members ):
    # This function computes all eqbm
    # metrics for an entire ens array w/
    # dims [ timestep, member, gridpt ]
    # and outputs a dict of 1d arrays
    # with dimensionx [ timestep ]

    # Metrics computed include:
    # -Ens Mean      (1st central moment)
    # -Ens Std Dev   (2nd central moment)
    # -Ens Skew      (3rd central moment)
    # -Ens Kurtosis  (4th central moment)
    # -Ens Eqbm (only useful for const F!)

    # NOTE: this functions first computes 
    # the eqbm metrics of each gridpoint 
    # seperately, and then takes the RMS
    # of all gridpoints to find the 'ens value'

    # Reducing x3d size by using float32 -
    # prevents OOMKILL
    x3d = x3d.astype(np.float32)

    # Computing the model-mean of each gridpoint
    # at each time step:
    gridpt_means_2d = np.mean( x3d, axis=1 )

    # Computing the model-sigmas of each gridpoint
    # at each time step:
    gridpt_stddevs_2d = np.std( x3d, axis=1 )

    # Computing the model-skew of each gridpoint
    # at each time step by first calculating the
    # 3rd central moment:
    m3_2d = ( 1/num_members ) * np.sum( (x3d - gridpt_means_2d[:,None,:] )**3, axis=1 ) 
    gridpt_skews_2d = m3_2d / ( gridpt_stddevs_2d**3 )

    # Computing the model-kurtosis of each gridpoint
    # at each time step by first calculating the
    # 4th central moment:
    # NOTE: this is 'excess' kurtosis to compare to
    # a Gaussian distribution (kurt=0)
    m4_2d = ( 1/num_members ) * np.sum( (x3d - gridpt_means_2d[:,None,:] )**4, axis=1 ) 
    gridpt_kurts_2d = m4_2d / ( gridpt_stddevs_2d**4 ) - 3.0

    # Now taking the root-mean-square of each
    # of these metrics across the entire latitude
    # rings to find the 'model-average' mean,
    # sigma, skew, and kurtosis at every time-step.
    #
    # Basically asking, "at a random gridpoint,
    # & some given time, what is the average 
    # distribution?"

    model_mean_1d = np.sqrt( np.mean( gridpt_means_2d ** 2, axis=1 ) )

    model_std_dev_1d = np.sqrt( np.mean( gridpt_stddevs_2d ** 2, axis=1 ) )

    model_skew_1d = np.sqrt( np.mean( gridpt_skews_2d ** 2, axis=1 ) )

    model_kurt_1d = np.sqrt( np.mean( gridpt_kurts_2d ** 2, axis=1 ) )

    # Storing into a dictionary with the keys:
    # 'mean', 'std_dev', 'skew', 'kurt',
    data_dict = {}
    data_dict[ 'mean' ] = model_mean_1d
    data_dict[ 'std_dev' ] = model_std_dev_1d
    data_dict[ 'skew' ] = model_skew_1d
    data_dict[ 'kurt' ] = model_kurt_1d

    # Now computing the final eqbm values of each 
    # metric. NOTE: this assumes that the model has
    # a constant F, and has already been run to eqbm
    for key in data_dict:
        eqbm_val = np.mean( data_dict[key][-19:] )
        # Storing back into dictionary
        save_key = 'eqbm_' + key
        data_dict[save_key] = eqbm_val

    return data_dict