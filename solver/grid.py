#################################
#          ╔═╗╦═╗╦╔╦╗           #
#          ║ ╦╠╦╝║ ║║           #
#          ╚═╝╩╚═╩═╩╝           #
#                               #
# Defines a grid by which to    #
# solve on                      #
#################################

# Important modules
# from collections.abc import Iterable
from numpy import zeros

# Generates a grid
def grid(dim:int, n_points:int, n_vars:int):
    return [zeros((n_points,)*dim) for i in range(n_vars)]
