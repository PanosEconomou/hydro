# Hydro

Relativistic Hydrodynamics Solver.

So far the solver is just stupid classical hydrodynamics lol. SOON SOON

## Prerequisites

The solver can handle any dimension you give it, however, there are two scripts provided that solve a shock tube problem in 1 and and 2 dimensions respectively. To run them one will need to have the following packages installed and `python > 3.6`

```
numpy
matplotlib
tqdm
```
the last one is just to make the progress bars look pretty :)

## How to RUN

You can run wither script in a similar way by running. 

```shell
$ python 2D_shock.py
```

You can find help about how to run with different parameters using
```shell
$ python 2D_shock.py -h

usage: 2D Shock Tube Hydro Solver [-h] [-n N_POINTS] [-L LENGTH] [-g GAMMA] [-T DT]
                                  [-S {circle,square,offset_square}] [-P PRESSURE]
                                  [-F FRAMES] [-o OUTPUT]

options:
  -h, --help            show this help message and exit
  -n N_POINTS, --n_points N_POINTS
                        Number of points per axis
  -L LENGTH, --length LENGTH
                        Length in Meters
  -g GAMMA, --gamma GAMMA
                        Adiabatic constant of fluid
  -T DT, --dt DT        Timestep
  -S {circle,square,offset_square}, --shape {circle,square,offset_square}
                        What is the shape of the discontinuity
  -P PRESSURE, --pressure PRESSURE
                        Pressure peak of the shockwave
  -F FRAMES, --frames FRAMES
                        Number of timesteps for the simulation
  -o OUTPUT, --output OUTPUT
                        The file to output
```