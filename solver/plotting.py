
#################################
#          ╔═╗╦  ╔═╗╔╦╗         #
#          ╠═╝║  ║ ║ ║          #
#          ╩  ╩═╝╚═╝ ╩          #
#                               #
# Plots the data nicely in      #
# interactive windows           #
#################################            

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from .HLL import get_quantities

def plot(U,gamma,*args,**kwargs):
    # PLOT AS ANIMATION
    fig = plt.figure(figsize=(5,5))
    axR = fig.add_subplot(221)
    axP = fig.add_subplot(222)
    axE = fig.add_subplot(223)
    axC = fig.add_subplot(224)

    # Prettify
    ax = [axR,axP,axC,axE]
    for axis in ax: 
        axis.set_yticklabels([])
        axis.set_xticklabels([])
        axis.set_xticks([])
        axis.set_yticks([])

    axR.set_title('Density')
    axP.set_title('Pressure')
    axE.set_title('Energy Density')
    axC.set_title('Speed of Sound')

    V,P,F,e,c = get_quantities(U[0],gamma)
    showR = axR.imshow(U[0][0],interpolation='bicubic',cmap='viridis')
    showP = axP.imshow(P,interpolation='bicubic',cmap='Blues')
    showE = axE.imshow(e,interpolation='bicubic',cmap='YlOrRd')
    showC = axC.imshow(c,interpolation='bicubic',cmap='BuGn')

    def update(frame):
        V,P,F,e,c = get_quantities(U[frame],gamma)
        showR.set_array(U[frame][0])
        showP.set_array(U[frame][0])
        showE.set_array(U[frame][0])
        showC.set_array(U[frame][0])

        return showR,showP,showE,showC

    animation = FuncAnimation(fig=fig,func=update, frames=len(U), interval=1,blit=True)
    return fig,[axR,axP,axE,axC],animation