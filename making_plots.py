#Antoine
#time to start making some plots

import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def plot_scatter(curves, colors=['blue','red'], make_label=False, \
                labels=['H','C'], widths=[1.,1.], zero=False, one=False, xlabel='Julian Date', \
                ylabel='Flux', xlims = [None, None], ylims=[None, None], \
                markers = ['.','+'], sizes=[1.,1.], save_name='', \
                xticks=np.array([]), yticks=np.array([]), grid=False):
    """
    curves is a list of pairs of arrays to plot
    curves =  [[x1,y1],[x2,y2],... ]
    """
    fig,ax = plt.subplots()
    plt.tight_layout()
    fig.dpi=100
    #fig.figsize=(6,3)
    fig.set_size_inches(7,4)
    # gridlines
    if grid:
        ax.set_axisbelow(True)
        ax.grid(visible=True,which='major',axis='y',zorder=0,alpha=0.4)
    # plotting the numbers
    for i in range(len(curves)):
        ax.scatter(curves[i][0],curves[i][1],color=colors[i],\
        label=labels[i], marker=markers[i], s=sizes[i], linewidth=widths[i])
        #
    # constant hlines
    if zero: ax.hlines((0.),linewidth=0.7,color='k',xmin=curves[0][0][0],xmax=curves[0][0][-1]*1.1)
    if one: ax.hlines((1.),linewidth=0.7,color='k',xmin=curves[0][0][0],xmax=curves[0][0][-1]*1.1)
    # labels on x and y axes
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    # ticks on x and y
    if xticks.size>1: ax.set_xticks( xticks )
    if yticks.size>1: ax.set_yticks( yticks )
    # limits on x and y axes
    ax.set_ylim(ylims)
    ax.set_xlim(xlims)
    # label 
    if make_label: ax.legend(loc='best')
    # saving
    if save_name:
        figdat = {'Author':'Antoine Darius','Software':'making_plots.py'}
        plt.savefig(save_name,metadata=figdat,bbox_inches='tight',dpi=fig.dpi)
    plt.show()
    return
def plot_lines(curves, colors=['blue','red'], labels=['H','C'], zero=False):
    """
    curves is a list of pairs of arrays to plot
    curves =  [[x1,y1],[x2,y2],... ]
    """
    fig,ax = plt.subplots()
    fig.dpi=140
    fig.figsize=(6,3)
    #
    for i in range(len(curves)):
        ax.plot(curves[i][0],curves[i][1],color=colors[i],label=labels[i], lw=1.)
        #
    if zero: ax.hlines((0.),linewidth=0.7,color='k',xmin=curves[0][0][0],xmax=curves[0][0][-1])
    ax.set_ylabel('Flux')
    ax.set_xlabel('Julian Date')
    ax.legend(loc='best')
    #
    plt.show()
    return

if __name__ == '__main__':
    saving_folder = '/home/antojr/codespace/plots/'
    data_dir_1 = '/home/antojr/codespace/results_code/'
    #data loading
    a = np.load('a_cometmeta.npy')
    #dat, h1, c1, d1, flag1 = np.loadtxt("/home/antojr/stash/datatxt/gascurves_x4_424km-corrected.txt",dtype=float,unpack=True,skiprows=1)
    dat = a['julian date'].copy()
    gas_data = np.load(data_dir_1 + 'gascurves_x5-dorrect.npy')
    h1, c1, d1, flag1 = gas_data['h2o'],gas_data['co2'],gas_data['dust'],gas_data['clip flag']
    # weeding out bad data
    check_for_nucleus =  np.abs(c1) > 1e-3
    c1_mask = c1.copy()[ check_for_nucleus ]
    h1_mask = h1.copy()[ check_for_nucleus ]
    dat_mask = dat.copy()[ check_for_nucleus ]
    #



    #plot_making
    ratio_plot=False
    gascurve_plot=True

    if ratio_plot:
        #make the ratio plot
        ratty = c1_mask / h1_mask
        plotting = [[dat_mask,ratty ] ]
        ratplotxlims = 2455506.0, 2455515.0
        ratplotylims = -.2, 1.3
        plot_scatter( plotting, colors = ['purple'], ylabel = 'Flux Ratio, $CO_2$/$H_2O$', make_label=False, \
        xlims = ratplotxlims, ylims = ratplotylims, one=True, save_name=saving_folder+ 'paper_gasratio.png' )

    ## gas curves plots ##
    if gascurve_plot:
        # plotting the h2o and co2 gascurves
        y_h, y_c = h1_mask, c1_mask
        x_time = dat_mask
        # converting julian date to encounter date
        enc = 2455505.0831866
        encdate = x_time - enc
        plotty = [ [encdate, y_h/1e8] , [encdate, y_c/1e8] ]
        ## plotting params
        # limits
        prehalf = 5.25 ; poshalf = 6.50 ; hourmargin = 1. / 24.
        x1 = encdate[0] - hourmargin*2.
        x2 = x1 + prehalf
        x4 = -0.9
        x3 = x4 - prehalf
        x5 = 0.5
        x6 = x5 + poshalf
        x8 = encdate[-1] + hourmargin*2.
        x7 = x8 - poshalf
        xlim4 = [ (x1, x2), (x3, x4), \
                (x5,x6), ( x7 , x8 ) ]
        ylim4 = [(-0.19,0.9), (-0.19,1.14), (0,1.12), (-0.080,0.9)] #handpicked by eye to feature the data
        # markers
        marking = ['.','.']
        sizing = [ 30.,30. ]
        widing = [1.2,1.2]
        # tick marks
        gas_xtick = np.arange( -11.,15.5,0.5 )
        gas_ytick = np.arange( -0.2,1.3,0.1 )
        # save names
        saving_gases = ['gascurve1.png','gascurve2.png','gascurve3.png','gascurve4.png' ]
        #for i in (0,1,2,3):
        for i in range(4):
            plot_scatter( plotty, make_label=False, zero=True, colors = ['tab:blue','tab:red'],\
                xlims = xlim4[i], ylims=ylim4[i], xlabel='Days from encounter', markers= marking, sizes=sizing, \
                xticks=gas_xtick, yticks=gas_ytick, grid=True, ylabel='$H_2O$,$CO_2$ Luminosity [$10^8$ W]',\
                save_name=saving_folder + saving_gases[i],widths=widing )

    ## fourier-lomb-scargle plots ##

    ## folding lightcurves plots ##

    ## differentials plots ##
    pass
    
else:
    pass
#ratio gas curves

