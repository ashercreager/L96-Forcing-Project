# This folder holds all code from the beginning stages of this project
# during SP26.

# This code is inefficient and hard to work with, and so my goal prior
# to SU26 is to streamline everything and make it much more flexible.

# The biggest problem currently is that my 'run_lorenz96' scripts aren't
# saving their output anywhere, meaning that the only way to draw a plot
# is to run the model at the same time, which wastes a ton of time.
# I end up running the same model solution several times trying to fix
# the way a plot looks when I could've just ran the model once and 
# saved its output somewhere. It also makes it really hard to work with
# the data from the model and change which parameters I want calculated.

# My current goal (5/2/2026) is to - instead of trying to cram everything
# into a single script like before - break the code up into their own
# individual scripts independent of eachother.

# For example: 1 script to run the model and save its output somwehere,
# another script to calculate eqbm metrics for that model run and save
# those somewhere, another script to plot, etc.

# One of my far-away goals is to eventually run 'ensembles-of-ensembles':
# for these larger datasets, I'll want to only save the output of the final
# super-ensemble solution instead of everysingle individual run. But for 
# the individual runs, saving the entire solution array should be good