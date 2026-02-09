import numpy as np

# dimensions [ens x gridpt]

arr = np.array( [ [2,4,20], [3,4,2], [4,4,2] ])  # 3 ensemble, 3 gridpoints

means = np.mean(arr, axis=0)
xc = arr - means

print(means)
print(xc)



arr2 = np.array([[2,2,2,2],[3,3,3,3],[4,4,4,4]])

arr3 = np.array([1,2,1,1])

print(arr2 - arr3)

# CONCLUSION: If array #1 is a 2d array with m columns (elements per sub-array)
# and n rows (total arrays), and array #2 is a 1d array with 4 m elements total,
# than array #1 + array #2 = the sum of each element of each subarray of #1
# with each element of array #2 respectively.