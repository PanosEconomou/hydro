# Import the libraries
from solver import *

# Import other cuties
import argparse
from tqdm.notebook import tqdm
from os.path import join, isdir, exists, isfile
from numpy import ogrid, sqrt
from matplotlib.animation import FFMpegWriter

# Create a parser for the parguments
parser = argparse.ArgumentParser(
    prog="2D Shock Tube Hydro Solver"
)

# Add useful arguments for the simulation
parser.add_argument('-n','--n_points',default=1000,help='Number of points per axis')
parser.add_argument('-L','--length',default=1,help='Length in Meters')
parser.add_argument('-g','--gamma',default=1.4,help='Adiabatic constant of fluid')
parser.add_argument('-T','--dt',default=0.0001,help='Timestep')
parser.add_argument('-P','--pressure',default=1,help='Pressure peak of the shockwave')
parser.add_argument('-F','--frames',default=5000,help='Number of timesteps for the simulation')
parser.add_argument('-o','--output',default=None,help='The file to output')


# Get the arguments
args = parser.parse_args()

# Create the shock tube parameters
n_points    = args.n_points
dim         = 1
n_vars      = 2+dim
dx          = args.length/n_points
gamma       = args.gamma
dt          = args.dt

# Create the grid
U =[grid(dim=dim,n_points=n_points,n_vars=n_vars)]

# Set the boundary conditions
U[0][0][:n_points//2]  = 1.000
U[0][0][n_points//2:]  = 0.100
U[0][2][:n_points//2]  = args.pressure/(gamma-1)
U[0][2][n_points//2:]  = 0.125/(gamma-1)

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