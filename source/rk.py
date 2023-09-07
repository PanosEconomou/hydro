#################################
#             ╦═╗╦╔═            #
#             ╠╦╝╠╩╗            #
#             ╩╚═╩ ╩            #
#                               #
# Using Runge-Kutta to solve    #
# the time dependance           #
#################################

from numpy import float64

def step(input:list, dt:float64, func, *params):
    Ui0 =  [      u +                  dt * f   for u,f     in zip(input,func(input,*params))]
    Ui1 =  [3/4 * u + 1/4 * u0 + 1/4 * dt * f   for u,u0,f  in zip(input,Ui0,func(Ui0,*params))]
    return [1/3 * u + 2/3 * u1 + 2/3 * dt * f   for u,u1,f  in zip(input,Ui1,func(Ui1,*params))]