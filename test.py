import pickle
import numpy as np

Fname = 'analyzed_data/Fconst/Fconst_6.5.pkl'
data = pickle.load( open(Fname, 'rb') )

print( data['F'] )