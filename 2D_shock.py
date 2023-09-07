# Import the libraries
from solver import *

# Import other cuties
import argparse
from tqdm.auto import tqdm
from os.path import join, isdir, exists, isfile
from numpy import ogrid, sqrt
from matplotlib.animation import FFMpegWriter

# Create a parser for the parguments
parser = argparse.ArgumentParser(
    prog="2D Shock Tube Hydro Solver"
)

# Add useful arguments for the simulation
parser.add_argument('-n','--n_points',default=100,help='Number of points per axis',type=int)
parser.add_argument('-L','--length',default=1,help='Length in Meters',type=float64)
parser.add_argument('-g','--gamma',default=1.4,help='Adiabatic constant of fluid',type=float64)
parser.add_argument('-T','--dt',default=0.001,help='Timestep',type=float64)
parser.add_argument('-S','--shape',choices=['circle','square','offset_square'],default='circle',help='What is the shape of the discontinuity')
parser.add_argument('-P','--pressure',default=10,help='Pressure peak of the shockwave',type=float64)
parser.add_argument('-F','--frames',default=500,help='Number of timesteps for the simulation',type=int)
parser.add_argument('-o','--output',default=None,help='The file to output')


# Get the arguments
args = parser.parse_args()

# Create the shock tube parameters
n_points    = args.n_points
dim         = 2
n_vars      = 2+dim
dx          = args.length/n_points
gamma       = args.gamma
dt          = args.dt

# Create the grid
U =[grid(dim=dim,n_points=n_points,n_vars=n_vars)]

# Set the boundary conditions
U[0][ 0][:]  = 0.1
U[0][-1][:] = 0.125/(gamma-1)

if args.shape == 'circle':
    def create_circular_mask(h, w, center=None, radius=None):

        if center is None: # use the middle of the image
            center = (int(w/2), int(h/2))
        if radius is None: # use the smallest distance between the center and image walls
            radius = min(center[0], center[1], w-center[0], h-center[1])

        Y, X = ogrid[:h, :w]
        dist_from_center = sqrt((X - center[0])**2 + (Y-center[1])**2)

        mask = dist_from_center <= radius
        return mask
    
    mask = create_circular_mask(*U[0][0].shape,radius=n_points*1/4)

    U[0][ 0][mask] = 1.00
    U[0][-1][mask] = args.pressure/(gamma-1)

elif args.shape == 'square':
    U[0][ 0][n_points//3:(2*n_points)//3,n_points//3:(2*n_points)//3] = 1.00
    U[0][-1][n_points//3:(2*n_points)//3,n_points//3:(2*n_points)//3] = args.pressure/(gamma-1)

elif args.shape == 'offset_square':
    U[0][ 0][n_points//3:(2*n_points)//3,n_points//3:(2*n_points)//4] = 1.00
    U[0][-1][n_points//3:(2*n_points)//3,n_points//3:(2*n_points)//4] = args.pressure/(gamma-1)

# With the boundary conditions set, we just need to solve
for i in tqdm(range(args.frames),desc='Solving...'): U.append(step(U[-1], dt, HLL_div, gamma ,dx))

# After we solve we just need to plot
fig,ax,animation = plot(U,gamma)

if args.output is not None: 
    filename = args.output
    if '.mp4' not in filename:
        if isdir(filename) and exists(filename):
            join(filename,'output.mp4')
        if isfile(filename):
            filename+='.mp4'

    FFwriter = FFMpegWriter(fps=50)
    animation.save(filename,writer=FFwriter)


plt.show()