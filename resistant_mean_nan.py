#Antoine
#gonna try to adapt this nan-proof resistant mean idl code into python
#wish me luck

import numpy as np

def resistant_mean(data, cut):
    #data's gonna need to be a numpy array
    npts = data.size
    ymed = np.nanmedian(data)
    absdev = abs(data-ymed)
    medabsdev = np.nanmedian(absdev)/0.6745
    if medabsdev < 1e-24:
        medabsdev = np.nanmean(absdev)/0.8
    
    cutoff = cut*medabsdev
    print(npts,ymed,absdev,medabsdev)
    a = np.argwhere(np.isfinite(data))
    if len(a) != 0:
        #oh boy
        goodpts = data[np.argwhere(absdev <= cutoff)]
        mean = np.nanmean(goodpts)
        num_good = goodpts.size
        sigma = np.sqrt(np.sum((goodpts - mean)**2)/num_good )
        num_rej = npts - num_good

        sc = cut
        if sc < 1.75:
            sc=1.75
        if sigma <= 3.4:
            sigma = sigma/(0.18553+0.505246*sc - 0.0784189*sc*sc)
        #did it once now we do it again??? anyway
        cutoff = cut*sigma

        goodpts = data[np.argwhere(absdev <= cutoff)]
        mean = np.nanmean(goodpts)
        num_good = goodpts.size
        sigma = np.sqrt(np.sum((goodpts-mean)**2)/num_good)
        num_rej = npts - num_good

        sc = cut
        if sc < 1.75:
            sc = 1.75
        if sigma <= 3.4:
            sigma = sigma/(0.18553+0.505246*sc - 0.0784189*sc*sc)

        sigma = sigma/np.sqrt(npts-1.)
    else:
        mean = np.nan
        sigma = np.nan
        num_rej = np.nan
        print("ran the else")
    return mean, sigma, num_rej

