
'''
    This script contains the main loop
    necessary to run the lorenz96 model
    on an entire ensemble across a 
    discretized latitude circle. Forcing 
    F can be a constant or variable function.

    When done running a single ensemble, script
    will dump eqbm metrics to a pickle file. 

'''

# Packages
import numpy as np
import matplotlib.pyplot as plt
import lorenz96_model as l96
from dataclasses import dataclass
import functions
import pickle


'''         MODEL-SETTINGS + DEFAULT VALUES        '''
@dataclass
class Config:
    # Number of grids along lat-ring
    num_gridpts : int = 40

    # Number of members in ens
    ens_size : int = 4000

    # How long model should run in time-steps
    # NOTE: total runtime in tau = dt * tot_runtime
    tot_runtime : int = 300

    # Ensuring reproducibility
    random_seed : int = 0

    # Save settings
    save_dir : str = ""
    save_name : str = ""

    # Other
    dt : float = 0.05 # currently unimplemented



# Spin-up function
def init_ensemble( cfg : Config, forcing_func ):
    ''' 
        Generates an initial-state (tau = 0) ensemble 
        of slightly perturbed members from a single
        reference member  
    '''

    # For reproducibility, reset random seed each call
    np.random.seed( cfg.random_seed )

    # Define the ensemble member which all other members will be perturbed from -
    # called the 'reference member'
    x_single = np.random.normal( loc=0, scale=1e-1, size=(1, cfg.num_gridpts) )

    # Let l96 run for 1000 steps on reference state so it attains model-accurate values
    x_single, _ = l96.multistep( x_single, 0, forcing_func, 2000 )

    # Create the 2d ensemble array of slightly perturbed members from the reference state
    x_ens2d_init = x_single + np.random.normal(
        loc=0,
        scale=1e-2, # SMALL PERTURBATIONS
        size=(cfg.ens_size, cfg.num_gridpts)
    )

    return x_ens2d_init




def Main( cfg : Config, forcing_func ):

    ''' Function to run l96 model to a specified
        number of steps on the entire ensemble

        Inputs : 
        - model settings (config class)
        - forcing function F
    '''

    # Defining x_ens2d before first simulation run
    x_ens2d = init_ensemble( cfg, forcing_func )

    # Initializing 3d numpy array to store x_ens2d
    # at each time-step --> this is the array which
    # gets input into compute_eqbm_metrics.
    x3d = np.zeros( (
        cfg.tot_runtime, 
        cfg.ens_size, 
        cfg.num_gridpts
    ) )

    # Initializing a 1d array to store F at
    # every timestep - useful for variable F
    F_tseries = np.zeros( cfg.tot_runtime )
    

    # Loop model over n consecutive steps
    tau = 0.
    for i in range( cfg.tot_runtime ):

        # Storing current step's x_ens2d
        x3d[i,:,:] = x_ens2d

        # Storing current step's F value
        F_tseries[i] = forcing_func( tau )
        
        # Advance state 1 step into the future
        x_ens2d, tau = l96.multistep( 
            x_ens2d, tau, forcing_func, 1 
        )

    # --------- End loop --------\ 
    print("Model run complete")

    # Computing eqbm metrics of model run
    analyzed_data = functions.compute_eqbm_metrics(
        x3d, cfg.ens_size 
    )
    print("Finished analyzing data")

    # Other variables to store into dumped pickle file
    analyzed_data['F'] = float( forcing_func(0) ) # ONLY USEFUL FOR FCONST

    analyzed_data['F_tseries'] = F_tseries # USEFUL FOR VARYING F

    # saving cfg values    
    analyzed_data['dt'] = cfg.dt
    analyzed_data['num_steps'] = cfg.tot_runtime
    analyzed_data['num_members'] = cfg.ens_size 
    analyzed_data['random_seed'] = cfg.random_seed

    # Dumping pickle file containing analyzed
    # data into correct location
    fname = cfg.save_dir + cfg.save_name + '.pkl'
    pickle.dump( analyzed_data, open( fname, 'wb' ) )
