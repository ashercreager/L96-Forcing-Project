import pickle
import numpy as np

Fname = 'analyzed_data/Fconst/Fconst_10.pkl'
data = pickle.load( open(Fname, 'rb') )

print( data['kurt'] )