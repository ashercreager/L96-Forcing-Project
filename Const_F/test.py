import numpy as np

arr = np.array([
    [11,12,13,14],
    [21,22,23,24],
    [31,32,33,34]
])

arr_len = len(arr.T) #transposes the array to get the # of cols
arrplus1 = np.hstack( (arr[ 0:: , 1:: ], arr[ 0:: , 0:1]) )




# testing file writing and reading
import csv

output_filename = "test_output.csv"

with open(output_filename)