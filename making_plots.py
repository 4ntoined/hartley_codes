#Antoine
#time to start making some plots

import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def plot_scatter(curves, kinds=None, colors=None, make_label=False, \
                labels=None, widths=None, zero=False, one=False, xlabel='Julian Date', \
                ylabel='Flux', xlims = [None, None], ylims=[None, None], \
                markers = None, sizes=None, save_name='', xlines=None, \
                xticks=np.array([]), yticks=np.array([]), grid=False):
    """
    curves is a list of pairs of arrays to plot
    curves =  [[x1,y1],[x2,y2],... ]
    """
    ### empty variables that break code ###
    #markers, sizes, widths, labels
    n_curves = len(curves)
    colorlist = ('tab:blue','tab:orange','tab:green','tab:red','tab:purple',\
        'tab:brown','tab:pink','tab:gray','tab:olive','tab:cyan')
    labellist = ('A','B','C','D','E','F','G')
    if kinds==None:
        kinds = [ 'scatter' for i in range(n_curves) ] 
    if colors==None:
        colors = colorlist[:n_curves]
    if labels==None:
        labels = labellist[:n_curves]
    if widths==None:
        widths = [ 1. for i in range(n_curves) ]
    if markers==None:
        markers = [ '.' for i in range(n_curves) ]
    if sizes==None:
        sizes = [ 1. for i in range(n_curves) ]
    #
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
    #if kind=='scatter':
    for i in range(len(curves)):
        if kinds[i] == 'scatter':
            ax.scatter(curves[i][0],curves[i][1],color=colors[i],\
            label=labels[i], marker=markers[i], s=sizes[i], linewidth=widths[i])
            #
        elif kinds[i] == 'line':
            ax.plot(curves[i][0],curves[i][1],color=colors[i],\
            label=labels[i], linewidth=widths[i])
            #
        else:
            plt.close()
            return 'Not a valid kind.'
    # constant hlines
    if zero: ax.hlines((0.),linewidth=0.7,color='k',xmin=curves[0][0][0],xmax=curves[0][0][-1]*1.1)
    if one: ax.hlines((1.),linewidth=0.7,color='k',xmin=curves[0][0][0],xmax=curves[0][0][-1]*1.1)
    if xlines: ax.vlines( xlines, linewidth=0.7, color='k', ymin=-100, ymax=100 )
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
    data_dir_2 = '/home/antojr/codespace/results_code/derivative_analysis/'
    #data loading
    a = np.load('a_cometmeta.npy')
    am = np.load('a2_cometmeta.npy')
    #dat, h1, c1, d1, flag1 = np.loadtxt("/home/antojr/stash/datatxt/gascurves_x4_424km-corrected.txt",dtype=float,unpack=True,skiprows=1)
    dat = a['julian date'].copy()
    dat_mask  =am['julian date'].copy()
    gas_data = np.load(data_dir_1 + 'gascurves_x5-eorrect.npy')
    h1, c1, d1 = gas_data['h2o'],gas_data['co2'],gas_data['dust']
    #
    # MRI data
    mri_data = np.load(data_dir_1+'mri_dorrect.npy')
    #derivative data loading
    derivs = []
    #time, mritime, c1, h1, m1, c2, h2, m2
    derivv = ('derivs_gastime.npy','derivs_mritime.npy','derivs_curve_h1.npy','derivs_curve_c1.npy', \
        'derivs_curve_m1.npy','derivs_curve_h2.npy','derivs_curve_c2.npy','derivs_curve_m2.npy')
    for i in range( 8 ): derivs.append( np.load(data_dir_2 + derivv[i]) )
    dtime, dmtime, dh1, dc1, dm1, dh2, dc2, dm2 = derivs
    #derivative zeros
    dzeros = []
    dzerov = ('derivs_index_h1.npy','derivs_index_c1.npy','derivs_index_m1.npy', \
        'derivs_index_h2.npy','derivs_index_c2.npy','derivs_index_m2.npy')
    for i in range(len(dzerov)): dzeros.append( np.load(data_dir_2 + dzerov[i]) )
    dih1, dic1, dim1, dih2, dic2, dim2 = dzeros
    #plot_making
    ratio_plot=False
    gascurve_plot=False
    deriv_plot=True

    if deriv_plot:
        mri14 = mri_data['14-pix'].copy()
        mri14 = mri14/np.mean(mri14)
        mri_dates = mri_data['date'].copy()
        xx = dtime.copy()
        xm = dmtime.copy()
        x2 = dat_mask.copy()
        yc1 = dc1.copy()
        yc2 = dc2.copy()
        yh1 = dh1.copy()
        yh2 = dh2.copy()
        ym1 = dm1.copy()
        ym2 = dm2.copy()
        yyc = c1/np.mean(c1)*4.
        yyh  = h1/np.mean(h1)*4.
        #curvo = [ [x2,yy ],[xx,yc1  ], [xx,yc2  ]  ]
        hydros = [ [x2,yyh ], [xx, yh1  ] ]
        carbos = [ [x2,yyc ], [xx, yc1  ] ]
        mriss = [ [mri_dates,mri14 ], [xm, ym1  ] ]
        carb_mri = [  [ xm, ym1 ],[ xx, yc1 ]  ] 
        hydr_mri = [  [ xm, ym1 ],[ xx, yh1 ]  ] 
        #plot_scatter( mriss, kinds=['scatter','line','line'], colors=['k','blue','green'], xlines= xm[dim1].tolist())
        #plot_scatter( carbos, kinds=['scatter','line','line'], colors=['k','blue','green'], xlines= xx[dic1].tolist())
        #plot_scatter( hydros, kinds=['scatter','line','line'], colors=['k','blue','green'], xlines= xx[dih1].tolist())
        plot_scatter( hydr_mri, kinds=['line','line'] )
    if ratio_plot:
        #make the ratio plot
        ratty = c1 / h1
        plotting = [[dat_mask,ratty ] ]
        ratplotxlims = 2455506.0, 2455515.0
        ratplotylims = -.2, 1.3
        plot_scatter( plotting, colors = ['purple'], ylabel = 'Flux Ratio, $CO_2$/$H_2O$', make_label=False, \
        xlims = ratplotxlims, ylims = ratplotylims, one=True, save_name=saving_folder+ 'paper_gasratio.png' )

    ## gas curves plots ##
    if gascurve_plot:
        # plotting the h2o and co2 gascurves
        y_h, y_c = h1, c1
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
        #saving_gases = []
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

