
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
from numpy import min,max

def plot(U,gamma,*args,**kwargs):
    # PLOT AS ANIMATION
    fig = plt.figure(figsize=(5,5))
    axR = fig.add_subplot(221)
    axP = fig.add_subplot(222)
    axE = fig.add_subplot(223)
    axV = fig.add_subplot(224)
    ax  = [axR,axP,axE,axV]

    axR.set_title('Density')
    axP.set_title('Pressure')
    axE.set_title('Energy Density')
    axV.set_title('Speed')

    V,P,F,e,c = get_quantities(U[0],gamma)
    if len(V) == 2:
        showR = axR.imshow(U[0][0],interpolation='bicubic',cmap='viridis')
        showP = axP.imshow(P,interpolation='bicubic',cmap='Blues')
        showE = axE.imshow(e,interpolation='bicubic',cmap='YlOrRd')
        showV = axV.imshow(sum([v**2 for v in V])**0.5,interpolation='bicubic',cmap='BuGn')
        
        # Prettify
        for axis in ax: 
            axis.set_yticklabels([])
            axis.set_xticklabels([])
            axis.set_xticks([])
            axis.set_yticks([])


    if len(V) == 1:
        showR, = axR.plot(U[0][0],c='green',*args,*kwargs)
        showP, = axP.plot(P,c='blue',*args,*kwargs)
        showE, = axE.plot(e,c='orange',*args,*kwargs)
        showV, = axV.plot(V[0],c='red',*args,*kwargs)

        plt.tight_layout()

    def update(frame):
        V,P,F,e,c = get_quantities(U[frame],gamma)

        if len(V) == 2:
            showR.set_array(U[frame][0])
            showP.set_array(P)
            showE.set_array(e)
            vv = sum([v**2 for v in V])**0.5
            showV.set_array(vv)
            showV.set(clim=(min(vv),max(vv)))

        if len(V) == 1:
            MAX = max(U[frame][0]), max(P), max(e), max(V[0])
            MIN = min(U[frame][0]), min(P), min(e), min(V[0])


            showR.set_ydata(U[frame][0])
            showP.set_ydata(P)
            showE.set_ydata(e)
            showV.set_ydata(V[0])

            for axis, Min, Max in zip(ax,MIN,MAX):
                LIM = axis.get_ylim()
                if LIM[0] > Min: axis.set_ylim(Min, LIM[1])
                if LIM[1] < Max: axis.set_ylim(LIM[0], Max)

        return showR,showP,showE,showV

    animation = FuncAnimation(fig=fig, func=update, frames=len(U), interval=1, blit=len(V)==2)
    return fig,ax,animation