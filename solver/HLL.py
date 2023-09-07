#################################
#           ╦ ╦╦  ╦             #
#           ╠═╣║  ║             #
#           ╩ ╩╩═╝╩═╝           #
#                               #
# Given some grids, it          #
# estimates the HLL solution    #
#################################

from .grid import grid
from numpy import array, roll, float64, maximum, zeros

# Calculate the left boundary
def HLL_half_step(U:list, F:list, A_plus:array, A_minus:array, dir:int, axis:int):
    assert dir != 0
    if dir > 0:
        return [(A_plus*f + A_minus*roll(f,dir,axis) + A_plus*A_minus * (u - roll(u,dir,axis)))/(A_plus + A_minus) for u,f in zip(U,F)]
    else:
        return [(A_plus*roll(f,dir,axis) + A_minus*f + A_plus*A_minus * (roll(u,dir,axis) - u))/(A_plus + A_minus) for u,f in zip(U,F)]

# Calculate the coefficient matrices
def HLL_A_pm(V:array, c:float64, dir:int, axis:int):
    assert dir != 0
    A_plus  = maximum(zeros(V.shape), maximum(V + c, roll(V,dir,axis) + c))
    # A_plus  = maximum(A_plus, maximum(V - c, roll(V,dir,axis) - c))
    A_minus = maximum(zeros(V.shape), maximum(- (V - c), - (roll(V,dir,axis) - c)))
    # A_minus = maximum(A_minus, maximum(- (V + c), - (roll(V,dir,axis) + c)))

    return A_plus, A_minus

# Calculate the divergence for a specific axis
def HLL_div_axis(U:list, F:list, V:array, c:float64, dx:float64, axis:int):
    F_plus  = HLL_half_step(U,F[axis],*HLL_A_pm(V[axis], c, +1, axis), +1, axis)
    F_minus = HLL_half_step(U,F[axis],*HLL_A_pm(V[axis], c, -1, axis), -1, axis)

    return [(f_minus - f_plus)/dx for f_minus,f_plus in zip(F_minus,F_plus)] 

# Extract the useful quantities
def get_quantities(U:list,gamma:float64):
    V = [U[i]/U[0] for i in range(1,len(U)-1)]
    # V = U[1]/U[0]
    e = U[-1]/U[0] - sum([v**2 for v in V])/2
    P = (gamma-1)*U[0]*e
    F = [[U[i].copy()] + [(U[i]*V[j-1] + (P if i==j else 0)) for j in range(1,len(U)-1)] + [(U[-1] + P)*V[i-1]] for i in range(1,len(U)-1)]
    # F = [U[1].copy(), U[1]*V + P, (U[2] + P)*V]
    c = (gamma*(gamma-1)*e)**0.5

    return V, P, F, e, c

# Calculate and return teh divergence for all the axes
def HLL_div(U:list, gamma:float64, dx:float64, quant = get_quantities):
    # Extract the useful quantities
    V, P, F, e, c = quant(U, gamma)

    # Calculate the new Flux
    F_news = [HLL_div_axis(U,F,V,c,dx,i) for i,_ in enumerate(U[0].shape)]
    return [sum(f[i] for f in F_news) for i in range(len(F_news[0]))]

