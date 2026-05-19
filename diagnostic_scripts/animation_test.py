import numpy as np
import pickle
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# loading x3d array
# dimensions: [time, ens member, gridpt]
fname = 'raw_output/Fosc/Fosc_1.0_year.pkl'
x3d = pickle.load( open(fname, 'rb') )

num_frames = x3d.shape[0]

# picking only 2 gridpts (x, x+1):
x2d_1 = x3d[:,:,0]
x2d_2 = x3d[:,:,1]



# animation
fig, ax = plt.subplots( figsize=(8,8) )
scat = ax.scatter([],[])

# setting fixed window limits
xmin = np.min( x3d[:,:,0:2] )
xmax = np.max( x3d[:,:,0:2] )
ax.set_xlim( xmin - 1, xmax + 1 )
ax.set_ylim( xmin - 1, xmax + 1 )

def update(frame):
    x = x2d_1[frame,:]
    y = x2d_2[frame,:]

    scat.set_offsets( np.column_stack([x,y]) )
    
    return scat,

ani = FuncAnimation(fig, update, frames=num_frames, interval=100, blit=True)

ani.save("diagnostic_scripts/test_anim.mp4", fps=30)

plt.close()