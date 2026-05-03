'''
    This script contains the main loop
    necessary to run the lorenz96 model
    on an entire ensemble across a 
    discretized latitude circle. Forcing 
    F can be a constant or variable function.

    When running a single ensemble, script
    can dump entire model solution to a 
    pickle file. 

    ( For super ensembles, this
    should probably be turned off. )
'''

# Packages
import numpy as np
import matplotlib.pyplot as plt
import lorenz96_model as l96


'''         MODEL-SETTINGS + DEFAULT VALUES        '''
class config:
    num_gridpts : int = 40   # number of grids along lat-ring
    ens_size    : int = 4000 # number of members in ens
    tot_runtime : int = 300  # how long model should run (steps)
    # NOTE: runtime in tau is given by dt * tot_runtime
    random_seed : int = 0
    save_dir    : str 
    F_attribute : str # Forcing attribute, used to describe data 
    dt          : float = 0.05 # currently unimplemented


# Spin-up function
def init_ensemble( cfg : config, forcing_func ):
    ''' 
        Generates an initial-state (tau = 0) ensemble 
        of slightly perturbed members from a single
        reference member  
    '''

    # For reproducibility, reset random seed each call
    np.random.seed( cfg.random_seed )

    # Define the ensemble member which all other members will be perturbed from (reference member)
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


def main( cfg : config, forcing_func ):

    ''' Function to run l96 model to a specified
        number of steps on the entire ensemble

        Inputs : 
        - model settings (config class)
        - forcing function F
    '''

    # Defining x_ens2d before first simulation run
    x_ens2d = init_ensemble( cfg, forcing_func )


    # Checking that a proper save directory has been
    # provided - if not, quit program
    if cfg.save_dir is None:
        print( 'ERROR: no save directory provided in running model' ) 
        print( 'Nothing to do with model output, quitting...' )
        quit()

    # Loop model over n consecutive steps
    tau = 0.
    for i in range( cfg.tot_runtime ):

        # Dump data as pickle file
        # TODO: ACTUALLY save data somewhere
        # Advance state 1 step into the future
        x_ens2d, tau = l96.multistep( 
            x_ens2d, tau, forcing_func, 1 
        )

    # --------- End loop --------\ 
    
